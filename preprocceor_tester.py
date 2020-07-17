from preprocessor import Preprocessor

thresh = 8

pre = Preprocessor(thresh)

# pre.process_data_for_labels('NFLX')
#
# pre.extract_featureSets('NFLX')

pre.do_ml('BAC')