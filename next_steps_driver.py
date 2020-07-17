from next_steps import DataAcquisition


reload_sp = False


da = DataAcquisition()

da.save_sp500_tickers()

da.get_data_from_yahoo(reload_sp)

da.combine_data()

da.visualize_data()