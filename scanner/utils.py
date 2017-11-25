	
import time, datetime

def rsi(close_prices):
	# Compute for first average gain and loss
	ave_gain = 0
	ave_loss = 0

	for i in range(1, 14):
		change = close_prices[i] - close_prices[i - 1]

		if change > 0:
			ave_gain += change
		else:
			ave_loss += change

	ave_gain /= 14
	ave_loss /= -14

	print("first ave gain: " + str(ave_gain))
	print("first ave loss: " + str(ave_loss))

    # Compute for succeeding average gain and loss
	for i in range(14, len(close_prices)):

		change = close_prices[i] - close_prices[i - 1]
		ave_gain, ave_loss, rsi = update_rsi(ave_gain, ave_loss, change)

	return ave_gain, ave_loss, rsi

def update_rsi(ave_gain, ave_loss, price_change):
	new_ave_gain = (ave_gain * 13 + (price_change if (price_change > 0) else 0)) / 14
	new_ave_loss = (ave_loss * 13 + (-price_change if (price_change < 0) else 0)) / 14

	if new_ave_gain == 0:	
		rsi = 0
	elif new_ave_loss == 0:
		rsi = 100
	else:
		rs = new_ave_gain / new_ave_loss	
		rsi = 100 - 100 / (1 + rs)

	return new_ave_gain, new_ave_loss, rsi

def btxdt_to_pydt(btx_dt):
	t = time.strptime(btx_dt, "%Y-%m-%dT%H:%M:%S")
	dt = datetime.datetime.fromtimestamp(time.mktime(t))

	return dt
