from fyers_api.Websocket import ws
from fyers_api import fyersModel
import datetime
import time
import creds
import symbol_generator
from connector import generate_access_token
import threading


client_id = creds.client_id
log_path = creds.log_path

orderplacetime = int(9) * 60 + int(45)
closingtime = int(13) * 60 + int(30)
universal_exit_time = int(15) * 60

long =symbol_generator.long
short = symbol_generator.short
symbols = symbol_generator.symbols

open_position = []

def getTime():
	return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def time_now():
	timenow = (datetime.datetime.now().hour * 60 + datetime.datetime.now().minute)
	return timenow

def custom_message(msg):
	# print(msg)
	script = msg[0]['symbol']
	ltp = msg[0]['ltp']
	high = msg[0]['high_price']
	low = msg[0]['low_price']
	ltt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(msg[0]['timestamp']))
	print(f"Script: {script}, Ltp:{ltp}, High:{high}, Low:{low}, ltt:{ltt}")
	
	if time_now() < closingtime:
		if (ltp <= low) and (script not in open_position) and (script in long):
			open_position.append(script)
			placeOrder("SELL", script, ltp)

		if (ltp >= high) and (script not in open_position) and (script in short):
			open_position.append(script)
			placeOrder("BUY", script, ltp)

def placeOrder(order, script, ltp):
	if order == "BUY":
		quantity = int(100)
		target_price = int(ltp*0.02)
		stoploss_price = int(ltp*0.01)

		order = fyers.place_order({"symbol":script,"qty":quantity,"type":"2","side":"1","productType":"BO","limitPrice":"0","stopPrice":"0","disclosedQty":"0","validity":"DAY","offlineOrder":"False","stopLoss":stoploss_price,"takeProfit":target_price})
		print(f"Buy Order Placed for {script}, at Price: {ltp} for Quantity: {quantity}, with order_id: {order['id']} at time: {getTime()}")
		print(open_position)
		
	else:
		quantity = int(1)
		target_price = int(ltp*0.0025)
		stoploss_price = int(ltp*0.01)

		order = fyers.place_order({"symbol":script,"qty":quantity,"type":"2","side":"-1","productType":"BO","limitPrice":"0","stopPrice":"0","disclosedQty":"0","validity":"DAY","offlineOrder":"False","stopLoss":stoploss_price,"takeProfit":target_price})
		print(f"Sell Order Placed for {script}, at Price: {ltp} for Quantity: {quantity}, with order_id: {order['id']} at time: {getTime()}")
		print(open_position)

def _websocket(newtoken):
	symbol = symbols
	data_type = "symbolData"
	fs = ws.FyersSocket(access_token=newtoken,run_background=False,log_path=log_path)
	fs.websocket_data = custom_message
	fs.subscribe(symbol=symbol,data_type=data_type)
	fs.keep_running()

def main():
	global fyers

	access_token = generate_access_token()
	fyers = fyersModel.FyersModel(token=access_token, log_path=log_path, client_id=client_id)
	fyers.token = access_token
	newtoken = f"{client_id}:{access_token}"

	while time_now() < orderplacetime:
		time.sleep(0.2)
	print(f"Time Now:{getTime()}, Initiating...")
	
	t = threading.Thread(target=_websocket(newtoken))
	t.start()
	if time_now() > universal_exit_time:
		positions = fyers.positions()['netPositions']
		if positions:
			data = {}
			fyers.exit_positions(data=data)

		else:
			print("No open positions")


if __name__ == "__main__":
	main()