import json

from pysam import AlignmentFile

from bam_feature_extractor.core.report import Report
from bam_feature_extractor.core.worker import Worker


class SequenceExtractor(Worker):
    description = """
    Create a file for each sequence (read) in the BAM file.

    Example:
    - <file_name>.1.txt
    - <file_name>.2.txt


    Contenu des fichiers:
    {
    "cigar": "74S42M2D13M3I173M4D3M11I91M64S",
    "flag": "0",
    "length": "0",
    "map_quality": "60",
    "name": "5854a906-28f5-49ac-8b5f-2bcaa9823b0a",
    "next_ref_name": "*",
    "next_ref_pos": "0",
    "qual": "++++++++",
    "ref_name": "contig_1",
    "ref_pos": "1395",
    "seq": "TTTTGTACTTCGTTGGTTACGTATTGCTACTTGCCTGTCGCTCTAT",
    "tags": [
        "NM:i:154",
        "ms:i:6079",
        "AS:i:6044",
        "nn:i:0",
        "tp:A:P",
        "cm:i:441",
        "s1:i:2777",
        "s2:i:0",
        "de:f:0.0339",
        "SA:Z:contig_1,110687,-,3510S71M1D3S,11,2;",
        "MD:Z:42^GA186^CATT1C1^C0G1G3T4A0A0T38^T119^GC42^AT34A42^G22^A",
        "rl:i:0"
    ]
}
    
    
    """

    def build_report(self, data: AlignmentFile, report: Report):
        for idx, _ in enumerate(data.fetch()):
            report.features[str(idx)] = json.dumps(_.to_dict(), sort_keys=True, indent=4)
