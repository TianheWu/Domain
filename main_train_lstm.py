from __Args import Args_lstm
from __Execution import Execution


args = Args_lstm()
# modify __Processing.py origin data
# modify train function
execution = Execution(args)
execution.prepare_data()
execution.train(args)