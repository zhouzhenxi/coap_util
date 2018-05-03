#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import threading
import struct
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox
from socket import *


root = Tk()
root.title('COAP test tool')

# Exit GUI cleanly
def _quit():
	root.quit()
	root.destroy()
	exit()

# Creating a Menu Bar
menuBar = Menu(root)
root.config(menu = menuBar)

# Add menu items
fileMenu = Menu(menuBar, tearoff = 0)
fileMenu.add_command(label = 'New')
fileMenu.add_separator()
fileMenu.add_command(label = 'Quit', command = _quit)
menuBar.add_cascade(label = 'File', menu = fileMenu)

def _test():
	messagebox.showinfo('Python Message Info Box', '通知：程序运行正常！') 

# Add a Menu to the Menu Bar and an item
setMenu = Menu(menuBar, tearoff = 0)
setMenu.add_separator()  
setMenu.add_command(label = 'Test', command = _test)
menuBar.add_cascade(label = 'Setting', menu = setMenu)

def _about():
	messagebox.showinfo('About', 'Version: 1.0.0')

# Add another Menu to the Menu Bar and an item
helpMenu = Menu(menuBar, tearoff = 0)
helpMenu.add_command(label = 'About', command = _about)
menuBar.add_cascade(label = 'Help', menu = helpMenu)

# Create Tab Control 
tabControl = ttk.Notebook(root)
# Create a tab
dataTab = ttk.Frame(tabControl) 
# Add the tab
tabControl.add(dataTab, text = 'Data Window')
# Add a second tab
rawDataTab = ttk.Frame(tabControl)
tabControl.add(rawDataTab, text = 'Raw Data')
logTab = ttk.Frame(tabControl)
tabControl.add(logTab, text = 'Message Log')
tabControl.pack(expand = 1, fill = 'both')

# URI
uriFrame = Frame(dataTab)
uriLabel = Label(uriFrame, text='COAP://')
uriLabel.pack(side = LEFT, anchor = W, padx = 10)
varUri = StringVar()
#varUri.set(gethostbyname(gethostname()))
varUri.set('192.9.25.75')
localIpEntry = Entry(uriFrame, textvariable = varUri);
localIpEntry.pack(side = RIGHT, anchor = W)
uriFrame.pack(anchor = W)

headerFrame = ttk.LabelFrame(dataTab, text='Header')
headerFrame.pack(anchor = W)

# message type
msgTypeFrame = Frame(headerFrame)
msgTypeLabel = Label(msgTypeFrame, text = 'Message Type:')
msgTypeLabel.pack(side = LEFT, anchor = W, padx = 10)
varMsgType = StringVar()
msgTypeCombox = ttk.Combobox(msgTypeFrame, textvariable = varMsgType)
msgTypeCombox['values'] = ('CON', 'NON', 'ACK', 'RST')
msgTypeCombox['state'] = 'readonly'
msgTypeCombox.current(0)
msgTypeCombox.pack(side = RIGHT, anchor = W)
msgTypeFrame.pack(anchor = W)


# requests
requestCodeFrame = Frame(headerFrame)
requestCodeLabel = Label(requestCodeFrame, text = 'Code:')
requestCodeLabel.pack(side = LEFT, anchor = W, padx = 10)
varRequestCode = IntVar()
getRadio = Radiobutton(requestCodeFrame, text = 'GET', variable = varRequestCode, value = 1)
getRadio.pack(side = LEFT, anchor = W, padx = 10)
postRadio = Radiobutton(requestCodeFrame, text = 'POST', variable = varRequestCode, value = 2)
postRadio.pack(side = LEFT, anchor = W)
putRadio = Radiobutton(requestCodeFrame, text = 'PUT', variable = varRequestCode, value = 3)
putRadio.pack(side = LEFT, anchor = W)
deleteRadio = Radiobutton(requestCodeFrame, text = 'DELETE', variable = varRequestCode, value = 4)
deleteRadio.pack(side = LEFT, anchor = W)
requestCodeFrame.pack(anchor = W)

#token
tokenFrame = Frame(headerFrame)
tokenLabel = Label(tokenFrame, text = 'Token:')
tokenLabel.pack(side = LEFT, anchor = W, padx = 10)
varToken = StringVar()
token_text = Entry(tokenFrame, textvariable = varToken);
token_text.pack(side = LEFT, anchor = W)
tokenFrame.pack(anchor = W)

#MID
midFrame = Frame(headerFrame)
midLabel = Label(midFrame, text = 'Message ID:')
midLabel.pack(side = LEFT, anchor = W, padx = 10)
varMid = StringVar()
midEntry = Entry(midFrame, textvariable = varMid);
midEntry.pack(side = LEFT, anchor = W)
midFrame.pack(anchor = W)

optionTreeItem = 0
def OnAddButton():
	global optionTreeItem
	optionTree.insert("", optionTreeItem, values = (optionCombox.get(), varOptionText.get()))
	optionTreeItem += 1
		
def OnDelButton():
	curr = optionTree.focus()
	if '' == curr:
		return
	optionTree.delete(curr)

# option
optionFrame = ttk.LabelFrame(dataTab, text='Option')
inputFrame = Frame(optionFrame)
optionLabel = Label(inputFrame, text = 'Option:')
optionLabel.pack(side = LEFT, anchor = W, padx = 10)
varOption = StringVar()
optionCombox = ttk.Combobox(inputFrame, textvariable = varOption)
optionCombox['values'] = ('', 'If-Match', 'Uri-Host', 'ETag', 'If-None-Match', 'Uri-Port', 
		'Location-Path', 'Uri-Path', 'Content-Format', 'Max-Age', 'Uri-Query', 
		'Accept', 'Location-Query', 'Proxy-Uri', 'Proxy-Scheme', 'Size1')
optionCombox['state'] = 'readonly'
optionCombox.current(0)
optionCombox.pack(side = LEFT, anchor = W)
optionTextLabel = Label(inputFrame, text = 'Value:')
optionTextLabel.pack(side = LEFT, anchor = W, padx=10)
varOptionText = StringVar()
optionEntry = Entry(inputFrame, textvariable = varOptionText);
optionEntry.pack(side = RIGHT, anchor = W)
inputFrame.pack(anchor = W)
operationFrame = Frame(optionFrame)
addButton = Button(operationFrame, text = 'Add', command = OnAddButton)
addButton.pack(side = LEFT, anchor = W, padx = 10)
deleteButton = Button(operationFrame, text = 'Delete', command = OnDelButton)
deleteButton.pack(side = LEFT, anchor = W, padx = 10)
operationFrame.pack(anchor = W)
optionTree = ttk.Treeview(optionFrame, show = 'headings', height = 6)
optionTree['columns'] = ('a', 'b')
optionTree.column('a', width = 150)
optionTree.column('b', width = 200)
optionTree.heading('a', text = 'option')
optionTree.heading('b', text = 'value')  
optionTree.pack(anchor = W)
optionFrame.pack(anchor = W)

# payload
payloadFrame = ttk.LabelFrame(dataTab, text = 'Payload')
scrolW = 80; scrolH = 5
varPayload = StringVar()
#payload_text = scrolledtext.ScrolledText(payloadFrame, width = scrolW, height = scrolH, wrap = WORD, textvariable = varPayload)
payloadEntry = Entry(payloadFrame, width = scrolW, textvariable = varPayload)
payloadEntry.pack(anchor = W)
payloadFrame.pack(anchor = W)

# raw data
rawDataFrame = ttk.LabelFrame(rawDataTab, text='Raw Data')
rawDataTree = ttk.Treeview(rawDataFrame, show = 'headings', height = 20)
rawDataTree['columns'] = ('a', 'b', 'c')
rawDataTree.column('a', width = 160)
rawDataTree.column('b', width = 60)
rawDataTree.column('c', width = 500)
rawDataTree.heading('a', text = 'Time')
rawDataTree.heading('b', text = 'Direction')
rawDataTree.heading('c', text = 'Data')
rawDataTree.pack(anchor = W)  
rawDataFrame.pack(anchor = W)

# message log
logFrame = ttk.LabelFrame(logTab, text='Message Log')
logTree = ttk.Treeview(logFrame, show = 'headings', height = 20)
logTree['columns'] = ('a', 'b', 'c', 'd', 'e', 'f')
logTree.column('a', width = 160)
logTree.column('b', width = 50)
logTree.column('c', width = 80)
logTree.column('d', width = 50)
logTree.column('e', width = 200)
logTree.column('f', width = 200)
logTree.heading('a', text = 'Time')
logTree.heading('b', text = 'Type')
logTree.heading('c', text = 'Token')
logTree.heading('d', text = 'MID')
logTree.heading('e', text = 'Options')
logTree.heading('f', text = 'Payload')
logTree.pack(anchor = W)  
logFrame.pack(anchor = W)

PORT = 5683
BUFFSIZE = 1024

def coapPackHeader(type, tkl, code, mid):
	ver = 1
	headerData = struct.pack('!BBH', ver << 6 | type << 4 | tkl, code, mid)
	return headerData
	
def coapPackToken(value):
	tokenData = value
	return tokenData

def coapPackOption(value, currentDelta):
	length = len(value)
	if length >= 269:
		lenTmp = 14
	elif length >= 13:
		lenTmp = 13
	else:
		lenTmp = length
	if currentDelta >= 269:
		optionDelta = struct.pack('BBB', (14 << 4) | lenTmp, (currentDelta - 269) >> 8, (currentDelta - 269) % 256)
	elif currentDelta >= 13:
		optionDelta = struct.pack('BB', (13 << 4) | lenTmp, currentDelta - 13)
	else:
		optionDelta = struct.pack('B', currentDelta << 4 | lenTmp)
	optionData = optionDelta
	if length >= 269:
		optionLen = struct.pack('BB', (length - 269) >> 8, (length - 269) % 256)
		optionData += optionLen
	elif length >= 13:
		optionLen = struct.pack('B', length - 13)
		optionData += optionLen
	else:
		pass
	optionData += value
	return optionData
	
def coapPackPayload(text):
	flag = struct.pack('B', 0xff)
	payloadData = flag
	payloadData += text
	return payloadData
	
def coapUnpackHeader(headerData):
	ver = (headerData[0] & 0xC0) >> 6
	if (ver != 1):
		print ('Err: version=%d' % ver)
		return 0, 0, 0, 0
	t = (headerData[0] & 0x30) >> 4
	tkl = headerData[0] & 0x0F
	code = headerData[1]
	mid = (headerData[2] << 8) | headerData[3]
	return t, tkl, code, mid
	
def coapUnpackToken(tokenData, offset, tkl):
	if tkl == 0:
		token = ''
	else:
		token = tokenData[offset : (offset + tkl)]
	return token
	
def coapUnpackOption(optionData, offset):
	delta = (optionData[offset] & 0xF0) >> 4
	len = optionData[offset] & 0x0F
	tempOffset = offset + 1
	if delta == 13:
		delta = optionData[tempOffset] + 13
		tempOffset += 1
	elif delta == 14:
		delta = (optionData[tempOffset] << 8 | optionData[tempOffset + 1]) + 269
		tempOffset += 2
	if len == 13:
		len = optionData[tempOffset] + 13
		tempOffset += 1
	elif len == 14:
		len = (optionData[tempOffset] << 8 | optionData[tempOffset + 1]) + 269
		tempOffset += 2
	option = optionData[tempOffset : tempOffset + len]
	optionLen = tempOffset + len - offset
	return delta, option, optionLen
	
def coapUnpackPayload(payloadData, packetLen, offset):
	tempOffset = offset + 1
	payload = payloadData[tempOffset : packetLen]
	return payload

messageTypeDict = {0 : 'CON', 1 : 'NON', 2 : 'ACK', 3 : 'RST'}

optionDict =   {'If-Match' : 1,
				'Uri-Host' : 3,
				'ETag' : 4,
				'If-None-Match' : 5,
				'Uri-Port' : 7,
				'Location-Path' : 8,
				'Uri-Path' : 11,
				'Content-Format' : 12,
				'Max-Age' : 14,
				'Uri-Query' : 15,
				'Accept' : 17,
				'Location-Query' : 20,
				'Proxy-Uri' : 35,
				'Proxy-Scheme' : 39,
				'Size1' : 60}

optionDictByValue = {1 : 'If-Match',
					 3 : 'Uri-Host',
					 4 : 'ETag',
					 5 : 'If-None-Match',
					 7 : 'Uri-Port',
					 8 : 'Location-Path',
					11 : 'Uri-Path',
					12 : 'Content-Format',
					14 : 'Max-Age',
					15 : 'Uri-Query',
					17 : 'Accept',
					20 : 'Location-Query',
					35 : 'Proxy-Uri',
					39 : 'Proxy-Scheme',
					60 : 'Size1'}

responseCodeDict = {'2.01' : 'Created',
					'2.02' : 'Deleted',
					'2.03' : 'Valid',
					'2.04' : 'Changed',
					'2.05' : 'Content',
					'4.00' : 'Bad Request',
					'4.01' : 'Unauthorized',
					'4.02' : 'Bad optionTree',
					'4.03' : 'Forbidded',
					'4.04' : 'Not Found',
					'4.05' : 'Method Not Allowed',
					'4.06' : 'Not Acceptable',
					'4.12' : 'Precondition Failed',
					'4.13' : 'Request Entity Too Large',
					'4.15' : 'Unsupported Content-Format',
					'5.00' : 'Internal Server Error',
					'5.01' : 'Not Implemented',
					'5.02' : 'Bad Geteway',
					'5.03' : 'Service Unavailable',
					'5.04' : 'Gateway Timeout',
					'5.05' : 'Proxying Not Supported'}

contentFormatDict ={0  : 'text/plain',
					40 : 'application/link-format',
					41 : 'application/xml',
					42 : 'application/octet-stream',
					47 : 'application/exi',
					50 : 'application/json'}


def OnButton():
	t = msgTypeCombox.current()
	tkl = len(varToken.get())
	if tkl > 8:
		messagebox.showinfo('Error', 'Token length is 0~8!')
		return
	code = varRequestCode.get()
	if code < 1 or code > 4:
		messagebox.showinfo('Error', 'Invalid request code!')
		return
	msgID = varMid.get()
	if '' == msgID:
		messagebox.showinfo('Error', 'message ID can not empty!')
		return
	messageID = int(msgID)
	temp_data = struct.pack('H', messageID)
	data = coapPackHeader(t, tkl, code, messageID)
	token = ''
	if (tkl > 0):
		token = varToken.get()
		data += coapPackToken(token.encode('utf-8'))
	children = optionTree.get_children()
	delta = 0
	optionValueTuple = ()
	for child in children:
		text = optionTree.item(child, 'values')
		optionNumber = optionDict[text[0]]
		delta = optionNumber - delta
		index = text[1].find('/')
		if (index < 0):
			data += coapPackOption(text[1].encode('utf-8'), delta)
		else:
			tempStr = text[1]
			tempDelta = delta
			while index >= 0:
				subStr = tempStr[0 : index]
				data += coapPackOption(subStr.encode('utf-8'), tempDelta)
				tempDelta = 0
				tempStr = tempStr[index + 1 : ]
				index = tempStr.find('/')
				if (index < 0):
					data += coapPackOption(tempStr.encode('utf-8'), tempDelta)
					break
		optionValueTuple += (text[0], text[1])
	payload = payloadEntry.get()
	if '' == payload:
		pass
	else:
		data += coapPackPayload(payload.encode('utf-8'))

	target = varUri.get()
	if '' == target:
		messagebox.showinfo('Error', 'URI can not empty!')
		return
	
	udpSocket = socket(AF_INET, SOCK_DGRAM)
	HOST = gethostbyname(gethostname())
	udpSocket.bind((HOST, PORT))
	
	print('Send the data:')
	for i in data:
		print ('%x ' % i, end = ' ')
	print('\n')
	addr = (target, PORT)
	udpSocket.sendto(data, addr)
	rawDataTreeItem = 0
	rawDataTree.insert("", rawDataTreeItem, values = (time.ctime(), '->', ','.join(['%02x' % i for i in data])))
	rawDataTreeItem += 1
	logTreeItem = 0
	logTree.insert("", logTreeItem, values = (time.ctime(), messageTypeDict[t], token, messageID, optionValueTuple, payload))
	logTreeItem += 1
	data, addr = udpSocket.recvfrom(BUFFSIZE)
	print('Receive the data:')
	for i in data:
		print ('%x ' % i, end = ' ')
	print('\n')
	packetLen = len(data)
	if packetLen < 4:
		print ('Err: data is wrong')
		return
	offset = 0
	t, tkl, code, mid = coapUnpackHeader(data)
	offset = 4
	print ('type=%d, tkl=%d, code=%d, mid=%d' % (t, tkl, code, mid))
	token = coapUnpackToken(data, offset, tkl)
	del optionValueTuple
	optionValueTuple = ()
	offset += tkl
	if (packetLen > offset):
		if (data[offset] != 0xFF):
			delta = 0
			while True:
				optionDelta, optionValue, optionLen = coapUnpackOption(data, offset)
				offset += optionLen
				delta += optionDelta
				if (delta == 12):
					TempValue = optionValue[0] << 8 | optionValue[1]
					optionValueTuple += (optionDictByValue[delta], contentFormatDict[TempValue])
				else:
					optionValueTuple += (optionDictByValue[delta], optionValue)
				if (packetLen == offset):
					break
				elif (packetLen > offset):
					if (data[offset] == 0xFF):
						payload = coapUnpackPayload(data, packetLen, offset)
						break
		else:
			payload = coapUnpackPayload(data, packetLen, offset)
	
	rawDataTree.insert("", rawDataTreeItem, values = (time.ctime(), '<-', ','.join(['%02x' % i for i in data])))
	rawDataTreeItem += 1
	if len(token):
		token = token.decode()
	if len(payload):
		payload = payload.decode()
	logTree.insert("", logTreeItem, values = (time.ctime(), messageTypeDict[t], token, mid, optionValueTuple, payload))
	logTreeItem += 1

	udpSocket.close()
	


sendFrame = Frame(dataTab)
runButton = Button(sendFrame, text = 'Send data', command = OnButton)
runButton.pack(side = LEFT, anchor = W, padx = 10)
sendFrame.pack(anchor=W)

# message loop
root.mainloop()
