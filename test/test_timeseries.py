import unittest
import pandas as pd
from pandas.testing import assert_frame_equal
import numpy as np
from functools import partial
from mytools import timeseries


df_input = pd.DataFrame({'id': ['1.01', '1.01', '2.02', '3.03' , '3.03'],
                         'date': pd.to_datetime(['2001-02-01', '2001-01-01', 
                                                 '2001-01-01', '2001-02-01', '2001-01-01']),
                         'feature': [False, False, False, True, True]},
                          index=[0, 1, 2, 3, 4])

df_expected_false = pd.DataFrame({'id': ['1.01', '1.01', '2.02'],
                                  'date': pd.to_datetime(['2001-01-01', '2001-02-01', 
                                                          '2001-01-01']),
                                  'feature': [False, False, False]},
                                   index=[1, 0, 2])

df_expected_event_delta = pd.DataFrame({'id': ['1.01', '1.01', '2.02', '3.03' , '3.03'],
                                        'date': pd.to_datetime(['2001-01-01', '2001-02-01', '2001-01-01', 
                                                                '2001-01-01', '2001-02-01']),
                                        'feature': [False, False, False, True, True],
                                        'feature_delta': [np.NaN, np.NaN, np.NaN, 0, 1]},
                                         index=[0, 1, 2, 3, 4])


def assert_df(left, right):
    return assert_frame_equal(left=left.sort_index(axis=1), 
                              right=right.sort_index(axis=1), check_dtype=False)


class TestUtilsFunctions(unittest.TestCase):
  
    def test_sample_id_hists(self):
        df_input_filtered = (df_input.groupby('id')
                                     .filter(lambda x: sum(x.feature) == 0))
        
        assert_df(timeseries.sample_id_hists(df_input_filtered, id_col='id', additional_sort_col='date', frac=1),
                  df_expected_false)
        
    
    def test_event_delta(self):
        assert_df(timeseries.event_delta(df_input, 'id', 'date', 'feature', period='M').reset_index(drop='id'),
                  df_expected_event_delta)

        
if __name__ == '__main__':
    unittest.main()
