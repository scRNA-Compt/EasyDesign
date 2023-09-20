import os
import os
import sys

import pandas as pd
import requests

import web.options.options as opt
from bin.design import reverse_complement
from web.model.model import Adaptor

mypath = opt.WORK_OUT_DIR
work_space_path = opt.WORK_SPACE

from fastapi import HTTPException


def runAdaptCmd(para: Adaptor) -> int:
    tmp_upload_url = f"http://127.0.0.1:{opt.SERVER_PORT}/upload_result"
    workpath = mypath + para.job_id + os.sep
    if not os.path.exists(workpath):
        os.makedirs(workpath)
    tmpcmdfile = workpath + "runAdapt.sh"
    cmd = "python " + work_space_path + "bin/design.py "
    if para.sliding_window:
        cmd = cmd + " sliding-window "
    else:
        cmd = cmd + " complete-targets "
    if para.fasta_file == "":
        inputfilename = workpath + "runAdapt.inputfile"
        ret = os.system("wget -q  -O " + inputfilename + " '" + para.fasta_url + "'")
        if ret != 0:
            raise HTTPException(status_code=501, detail="wget " + para.fasta_url + " failed with code " + str(ret))
        cmd = cmd + " fasta " + inputfilename
    else:
        cmd = cmd + " fasta " + para.fasta_file  # "examples/example.fasta "

    if para.specificity_url != "":
        specificfilename = workpath + "specific.fasta"
        ret = os.system("wget -q  -O " + specificfilename + " '" + para.specificity_url + "'")
        if ret != 0:
            raise HTTPException(status_code=501,
                                detail="wget " + para.specificity_url + " failed with code " + str(ret))
        cmd = cmd + " --specific-against-fastas " + specificfilename

    if para.sliding_window:
        cmd = cmd + " --window-size " + str(para.window_size)
        cmd = cmd + " --window-step " + str(para.window_step)
    else:
        cmd = cmd + " --best-n-targets " + str(para.bestntargets) + " "
        cmd = cmd + " -pl " + str(para.pl)
        cmd = cmd + " -pm " + str(para.pm)
        cmd = cmd + " -pp " + str(para.pp)
        cmd = cmd + " --obj-fn-weights " + str(para.objfnweights_a) + " " + str(para.objfnweights_b)
        if para.max_target_length > 0:
            cmd = cmd + " --max-target-length " + str(para.max_target_length)
        if para.max_primers_at_site > 0:
            cmd = cmd + " --max-primers-at-site " + str(para.max_primers_at_site)
        if para.primer_gc_hi > para.primer_gc_lo:
            cmd = cmd + " --primer-gc-content-bounds " + str(para.primer_gc_lo) + " " + str(para.primer_gc_hi)

    cmd = cmd + " --out-tsv " + workpath + "result "  # para.out_tsv
    cmd = cmd + " --obj "
    if para.obj:
        cmd = cmd + "maximize-activity "
    else:
        cmd = cmd + "minimize-guides "
    if para.ai_model == 'cas12a':
        cmd = cmd + " -gl " + str(para.gl + 4)  # add length of PAM
    else:
        cmd = cmd + " -gl " + str(para.gl)
    cmd = cmd + " --ai-model " + para.ai_model
    cmd = cmd + " --reversed " + str(para.reversed)
    cmd = cmd + " --id-m " + str(para.idm)
    cmd = cmd + " --cluster-threshold " + str(para.cluster_threshold)
    cmd = cmd + " --id-frac " + str(para.idfrac)
    modelname = para.ai_model
    classify_path = work_space_path + "easyDesign/models/classify/" + modelname
    regress_path = work_space_path + "easyDesign/models/regress/" + modelname
    print(classify_path)
    print(regress_path)
    if (not os.path.exists(classify_path)) or (not os.path.exists(regress_path)):
        raise HTTPException(status_code=501, detail="classify_path or regress_path does not exists")
    cmd = cmd + " --predict-activity-model-path " + classify_path + " " + regress_path + " "
    if para.unaligned_fasta:
        cmd = cmd + " --unaligned --mafft-path /usr/bin/mafft "
    if para.write_aln:
        cmd = cmd + " --write-input-aln " + workpath + "alignment "

    cmd = cmd + "  >> " + workpath + "runningprocess.o1 2>> " + workpath + "runningprocess.o2 "
    ret = os.system("echo '" + cmd + "' > " + tmpcmdfile)
    if ret != 0:
        return 1000 + ret
    ret += os.system(
        "echo 'ret=$?' >> " + tmpcmdfile)  # echo 'echo $? > " + para.out_tsv + ".finished' >> "+tmpcmdfile)
    if ret != 0:
        return 2000 + ret
    ret += os.system(
        "echo 'cd " + workpath + " >> " + workpath + "runningprocess.o1 2>> " + workpath + "runningprocess.o2 ' >> " + tmpcmdfile)
    if ret != 0:
        return 2800 + ret
    ret += os.system(
        "echo 'cat " + workpath + "runningprocess.o1 " + workpath + "runningprocess.o2 >> " + workpath + "log.txt' >> " + tmpcmdfile)
    if ret != 0:
        return 2600 + ret
    if ret != 0:
        return 2300 + ret
    ret += os.system("echo 'files=\"\"' >> " + tmpcmdfile)
    ret += os.system("echo 'for f in `ls -1 result*.tsv` ;do files=$files$f\",\";done' >> " + tmpcmdfile)
    if para.write_aln:
        ret += os.system("echo 'for f in `ls -1 alignment*.fasta` ;do files=$files$f\",\";done' >> " + tmpcmdfile)
    ret += os.system(
        "echo '/usr/bin/curl --location --request POST -X POST \"" + tmp_upload_url + "\" "
                                                                                               "--header \"User-Agent: " \
                                                                                               "Apipost client Runtime/+https://www.apipost.cn/\" --form \"uploadResultAddr="+para.upload_result_addr+"\" --form \"jobId=" + str(
            para.job_id) + "\"  >> " + workpath + "runningprocess.o1 2>> " + workpath + "runningprocess.o2 ' >> " + tmpcmdfile)
    if ret != 0:
        return 3000 + ret
    ret += os.system("echo 'echo $? > " + workpath + "curl.finished' >> " + tmpcmdfile)
    if ret != 0:
        return 4000 + ret
    ret = os.system("nohup /usr/bin/sh -x " + tmpcmdfile + " &")
    if ret != 0:
        return 5000 + ret
    ret = os.system("touch " + workpath + "runAdapt.started")
    return ret


def convert_and_upload(uploadResultAddr:str, jobId:str):
    upload_result_addr = uploadResultAddr + "/api/job/uploadResult"
    job_id = jobId
    result_path, log_path = convert_and_saveresult(job_id)
    file_result = ("resultFiles", ("result", open(result_path, mode="rb")))
    file_log = ("resultFiles", ("log", open(log_path, mode="rb")))
    resultFiles = [file_result, file_log]
    data = {
        "runStatus": 0,
        "jobId": job_id,
    }
    requests.post(upload_result_addr, data=data, files=resultFiles)


def convert_and_saveresult(job_id: str):
    input_dir = mypath + job_id + os.sep
    input_path = input_dir + "result.0.tsv"
    if not os.path.exists(input_path):
        input_path = input_dir + "result.tsv"
    result_content = pd.read_csv(input_path, index_col=None, sep="\t")
    rgb = result_content.groupby("guide-target-sequences", as_index=False)
    result_list = []
    rcl = result_content.columns.to_list()
    for guide, candidates in rgb:
        left_map = {}
        right_map = {}
        left_map_str = ""
        right_map_str = ""
        guide_info = (candidates.values[0][rcl.index("guide-expected-activities")], guide,
                      candidates.values[0][rcl.index("guide-target-sequence-positions")])
        for candidate in candidates.values:
            if len(left_map) <= 4: # left primer keep <=5
                left_start = candidate[rcl.index("left-primer-start")]
                if left_start not in left_map:
                    left_map[left_start] = (left_start, candidate[rcl.index("left-primer-target-sequences")])
            if len(right_map) <= 4: # right primer keep <=5
                right_start = candidate[rcl.index("right-primer-start")]
                if right_start not in right_map:
                    raw_seq = candidate[rcl.index("right-primer-target-sequences")]
                    reverse_seq = reverse_complement(raw_seq)
                    right_map[right_start] = (right_start, reverse_seq)
        for key in left_map:
            left_map_str = left_map_str + str(left_map[key]) + ","
        for key in right_map:
            right_map_str = right_map_str + str(right_map[key]) + ","
        result_list.append([guide_info, left_map_str, right_map_str])
    headers = ["guide-expected-activities", "guide-target-sequences", "guide-target-sequence-positions",
               "left-primer-target-sequences", "right-primer-target-sequences"]
    result_dir = mypath + job_id + os.sep + "result"
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)
    result_path = result_dir + os.sep + "result.0.tsv"
    log_path = mypath + job_id + os.sep + "log.txt"
    with open(result_path, "w") as outf:
        outf.write('\t'.join(headers) + '\n')
        lines = []
        for guide_info, left_map_str, right_map_str in result_list:
            guide_expected_activities, guide_target_sequences, guide_target_sequence_positions = guide_info
            line = [guide_expected_activities, guide_target_sequences, guide_target_sequence_positions, left_map_str,
                    right_map_str]
            lines.append(line)
        if len(lines) == 0:
            return result_path, log_path
        lines.sort(reverse=True)
        for w_line in lines:
            outf.write('\t'.join([str(x) for x in w_line]) + '\n')
    return result_path, log_path
