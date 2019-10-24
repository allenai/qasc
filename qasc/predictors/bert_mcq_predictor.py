from typing import cast, Tuple

from overrides import overrides

from allennlp.common.util import JsonDict, sanitize
from allennlp.data import Instance
from allennlp.data.dataset_readers import BertMCQAReader
from allennlp.predictors.predictor import Predictor


@Predictor.register('multiple-choice-qa-json')
class MultipleChoiceQAJsonPredictor(Predictor):
    """
    Wrapper for the bert_mc_qa model.
    """
    def _my_json_to_instance(self, json_dict: JsonDict) -> Tuple[Instance, JsonDict]:
        # Make a cast here to satisfy mypy
        dataset_reader = cast(BertMCQAReader, self._dataset_reader)

        question_data = json_dict['question']
        question_text = question_data['stem']
        choice_text_list = [choice['text'] for choice in question_data['choices']]
        choice_labels = [choice['label'] for choice in question_data['choices']]
        choice_context_list = []
        context = json_dict.get("para", None)
        for choice in question_data['choices']:
            choice_context_list.append(choice.get("para", None))
        instance = dataset_reader.text_to_instance(qid, question_text, choice_text_list,
                                                   context=context,
                                                   choice_context_list=choice_context_list)
        extra_info = {
            'id': json_dict['id'],
            'choice_labels': choice_labels
        }
        return instance, extra_info

    @overrides
    def _json_to_instance(self, json_dict: JsonDict) -> Instance:
        instance, _ = self._my_json_to_instance(json_dict)
        return instance

    @overrides
    def predict_json(self, inputs: JsonDict) -> JsonDict:
        instance, return_dict = self._my_json_to_instance(inputs)
        outputs = self._model.forward_on_instance(instance)

        answer_index = outputs['answer_index']
        answer = return_dict['choice_labels'][answer_index]
        score = max(outputs['label_probs'])

        return_dict['answer'] = answer
        return_dict['score'] = score
        return_dict['label_probs'] = outputs['label_probs']

        return sanitize(return_dict)