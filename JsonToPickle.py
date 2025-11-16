import pickle
import json
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

def json_to_pkl(json_file_path, pkl_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Convert dicts back to QuestionBlock objects recursively
    def deserialize(obj):
        if isinstance(obj, dict) and 'correctness' in obj:
            obj['correct_answers'] = set(obj.get('correct_answers', []))
            return QuestionBlock(**obj)
        if isinstance(obj, list):
            return [deserialize(x) for x in obj]
        return obj

    deserialized_data = deserialize(data)

    with open(pkl_file_path, 'wb') as f:
        pickle.dump(deserialized_data, f)

# Example usage
json_to_pkl('QuestionsWithCorrectChoice.json', 'QuestionsWithCorrectChoice.pkl')