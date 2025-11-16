import pickle
import json
from dataclasses import asdict, is_dataclass
from typing import List, Optional, Set
from dataclasses import dataclass, field

@dataclass
class QuestionBlock:
    correctness: str
    question: str
    choices: List[str]
    personal_comment: Optional[str]
    official_explanation: Optional[str]
    correct_answers: Set[str] = field(default_factory=set)
    right: Optional[bool] = None

def pkl_to_json(pkl_file_path, json_file_path):
    with open(pkl_file_path, 'rb') as f:
        data = pickle.load(f)

    # Convert dataclass objects to dicts recursively
    def serialize(obj):
        if is_dataclass(obj):
            result = asdict(obj)
            # Convert sets to lists for JSON
            if 'correct_answers' in result:
                result['correct_answers'] = list(result['correct_answers'])
            return result
        if isinstance(obj, list):
            return [serialize(x) for x in obj]
        return obj

    serialized_data = serialize(data)

    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(serialized_data, f, indent=4, ensure_ascii=False)

# Example usage
pkl_to_json('QuestionsWithCorrectChoice.pkl', 'QuestionsWithCorrectChoice.json')
