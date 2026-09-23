from copy import deepcopy
import pytest
from tools.compare_experiments import compare


def examples():
    first=dict(experiment='E1',model_id='synthetic-test-a',total=1,threshold=.7,
               dataset=[{'sha256':'synthetic-image','actual':'A'}],top1_accuracy=1,
               coverage=1,accuracy_among_accepted=1,accepted_correct_over_all=1)
    second=deepcopy(first);second.update(experiment='E2',model_id='synthetic-test-b')
    return first,second


def test_comparison_output():
    first,second=examples()
    assert '| Accuracy top 1 | 100.00% | 100.00% |' in compare(first,second)


@pytest.mark.parametrize('field,value',[('model_id','synthetic-test-a'),('threshold',.8),
    ('dataset',[{'sha256':'other-image','actual':'A'}]),('total',2),('coverage',float('nan'))])
def test_reject_incomparable_results(field,value):
    first,second=examples();second[field]=value
    with pytest.raises(ValueError):compare(first,second)


def test_no_accepted_predictions():
    first,second=examples();second.update(coverage=0,accuracy_among_accepted=None,accepted_correct_over_all=0)
    assert 'Tidak ditakrifkan' in compare(first,second)
