from pydantic import BaseModel


class Adaptor(BaseModel):
    fasta_file: str = ""            # url that can use to download a FASTA file, choose fasta_url or fasta_file as input
    fasta_url: str = ""             # fasta_file path, choose fasta_url or fasta_file as input
    specificity_url: str = ""       # specificity_url not supported yet
    bestntargets: int = 5           # number of results displayed at the end
    gl: int = 21                    # bare guide length
    pl: int = 30                    # primer length
    max_target_length: int = 250    # primer length + sgRNA length
    pm: int = 3                     # primer mismatches
    max_primers_at_site: int = 10   # -1
    idm: int = 4                    # differential identification mismatches
    pp: float = 0.98                # primer cover frac
    primer_gc_lo: float = 0.35      # primer gc low pct
    primer_gc_hi: float = 0.6       # primer gc high pct
    # maximum inter-cluster distance to use when clustering input sequences prior to alignment
    cluster_threshold: float = 0.3
    idfrac: float = 0.01            # lower values correspond to more specificity
    objfnweights_a: float = 0.5     # weights for penalties on primers
    objfnweights_b: float = 0.25    # weights for penalties on primers
    unaligned_fasta: bool = False   # to align FASTA sequences using MAFFT
    write_aln: bool = True          # write input aln
    sliding_window: bool = False    # no sliding_window means choose complete targets option
    window_step: int = 1            # window step, no use for complete targets option
    window_size: int = 200          # window size, no use for complete targets option
    obj: bool = 1                   # 0 for minimize-guides, 1 for maximize-activity
    job_id: str                     # distinguish different tasks
    context_nt: int = 10            # target_set =  context_nt + sgRNA + context_nt
    ai_model: str = "cas12a"        # differ cas-protein has differ AI model
    amplification_mode: str = "RPA" # eg: PCR、LAMP、RPA
    upload_result_addr: str         # dynamic url to upload result
    reversed: int = 0               # weather reversed. 0: no, 1:yes


class UploadResult(BaseModel):
    upload_result_addr: str         # the url for further processing the generated results
    job_id: str                     # distinguish different tasks