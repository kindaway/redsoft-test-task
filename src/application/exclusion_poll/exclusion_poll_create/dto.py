from src.application.common.dto import DTO


class ExclusionPollCreateDTO(DTO):
    exclusion_candidate_id: int
    reason: str
