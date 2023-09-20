from pydantic import BaseModel


class Adaptor(BaseModel):
    fasta_file: str = ""  # mypath+"examples/example.fasta " #input file path
    fasta_url: str = ""  # http://10.101.4.25:8000/upload/fasta/NC_002685.fasta"
    specificity_url: str = ""  # "http://10.101.4.25:8000/upload/custom_fasta/6264fd81bad2a076cda007a7.fasta" #"not supported yet, may url"
    bestntargets: int = 5  # tatget result num
    gl: int = 21
    pl: int = 30
    max_target_length: int = 250  # primer length + sgRNA length
    pm: int = 3
    max_primers_at_site: int = 10  # -1
    idm: int = 4
    pp: float = 0.98  # 1.0
    primer_gc_lo: float = 0.35  # 0.0
    primer_gc_hi: float = 0.6  # -1.0
    cluster_threshold: float = 0.3  # 0.2
    idfrac: float = 0.01
    objfnweights_a: float = 0.5
    objfnweights_b: float = 0.25
    unaligned_fasta: bool = False
    write_aln: bool = True
    sliding_window: bool = False
    window_step: int = 1
    window_size: int = 200
    obj: bool = 1  # 0 for minimize-guides, 1 for maximize-activity
    job_id: str
    context_nt: int = 10  # target_set =  context_nt + sgRNA + context_nt
    ai_model: str = "cas12a"  # differ cas-protein has differ AI model
    amplification_mode: str = "RPA"  # eg: PCR、LAMP、RPA
    upload_result_addr: str  # dynamic url to upload result
    reversed: int = 0  # weather reversed. 0: no, 1:yes


class UploadResult(BaseModel):
    upload_result_addr: str
    job_id: str
