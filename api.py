#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

import urllib.request
import urllib.parse

import xml.etree.ElementTree as ET

import sqlite3

#2029092
#x9SJvH5TfgJ1EfH2uD2qMXgeoCW5A5TE1VCgcPaAVJ7lJEQKqqUVgSo4zN6ZRJKx


class eve_api():
    def __init__(self):
        self.api_key = {"keyID":None, "vCode":None}
        self.db_names = ["transactions_db","journal_db"]
        self.connected = False
        self.keys = []
        self.encoding = None
        self.transactions = {}
        self.db = None
        self.cursor = None
        self.urls = {"base":"https://api.eveonline.com",
                     "account_balance":"/char/AccountBalance.xml.aspx",
                     "wallet_transactions":"/char/WalletTransactions.xml.aspx",
                     "wallet_journal":"/char/WalletJournal.xml.aspx",
                     "market_orders":"/char/MarketOrders.xml.aspx"}


    def import_api_key(self, path):
        with open(path, "r") as key_file:
            self.api_key["keyID"], self.api_key["vCode"] = key_file.read().split()


    def connect_db(self, name):
        if not self.db:
            self.db = sqlite3.connect(name)
            self.cursor = self.db.cursor()
            self.connected = True

    def disconnect_db(self):
        if self.db:
            self.db.disconnect()
            self.connected = False

    def create_transactions_table(self):
        self.cursor.execute('''create table if not exists transactions
                               (price float, clientName text, transactionType text, 
                               journalTransactionID int, stationID int, transactionFor text, 
                               typeID int, clientID int, transactionID int, quantity int, 
                               transactionDateTime datetime primary key,
                               typeName text, stationName text)''')


    def create_journal_table(self):
        self.cursor.execute('''create table if not exists journal
                                (argName1 text, ownerID1 int, ownerID2 int, date datetime primary key, 
                                taxAmount float, ownerName1 text, reason text, 
                                taxReceiverID int, ownerName2 text, amount float, refTypeID int, refID int, 
                                argID1 int, balance float)''')

    def encode_data(self, data):
        return bytes(urllib.parse.urlencode(data), 'utf-8')


    def get_page(self, url, data=None):
        if data == None:
            return urllib.request.urlopen(url)
        else:
            return urllib.request.urlopen(url, data)


    def manage_xml(self, page):
        return ET.fromstring(page.read())


    def import_transactions(self):
        page = self.get_page("%s/%s" % (self.urls["base"], self.urls["wallet_transactions"]), 
                                        self.encode_data(self.api_key))

        root = self.manage_xml(page)

        #if not self.keys:
        #    self.keys = tuple(list(page.iter('rowset'))[0].attrib['columns'].split(','))


        for item in root.iter('row'):
            self.cursor.execute('''insert or replace into transactions ('transactionDateTime', 'transactionID', 
                                  'quantity', 'typeName', 'typeID', 'price', 'clientID', 
                                  'clientName', 'stationID', 'stationName', 'transactionType', 
                                  'transactionFor', 'journalTransactionID') values (?,?,?,?,?,?,?,?,?,?,?,?,?)''', 
                                  (item.attrib['transactionDateTime'],
                                   item.attrib['transactionID'],
                                   item.attrib['quantity'],
                                   item.attrib['typeName'],
                                   item.attrib['typeID'],
                                   item.attrib['price'],
                                   item.attrib['clientID'],
                                   item.attrib['clientName'],
                                   item.attrib['stationID'],
                                   item.attrib['stationName'],
                                   item.attrib['transactionType'],
                                   item.attrib['transactionFor'],
                                   item.attrib['journalTransactionID']))


        root.clear()
        self.db.commit()

        
    def account_balance(self):
        page = self.get_page("%s/%s" % (self.urls["base"], self.urls["account_balance"]), 
                                        self.encode_data(self.api_key))
        root = self.manage_xml(page)
        
        #print(list(root.iter("row"))[0].attrib["balance"]) <-- save for later
        print("Balance: %s ISK" % (list(root.iter("row"))[0].attrib["balance"]))


    def import_journal(self):
        page = self.get_page("%s/%s" % (self.urls["base"], self.urls["wallet_journal"]), 
                                        self.encode_data(self.api_key))

        root = self.manage_xml(page)

        for item in root.iter("row"):
            self.cursor.execute('''insert or replace into journal (argName1, ownerID1, ownerID2, date, 
                                   taxAmount, ownerName1, reason, taxReceiverID, ownerName2, amount,
                                   refTypeID, refID, argID1, balance) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', 
                                   (item.attrib['argName1'],
                                   item.attrib['ownerID1'],
                                   item.attrib['ownerID2'],
                                   item.attrib['date'],
                                   item.attrib['taxAmount'],
                                   item.attrib['ownerName1'],
                                   item.attrib['reason'],
                                   item.attrib['taxReceiverID'],
                                   item.attrib['ownerName2'],
                                   item.attrib['amount'],
                                   item.attrib['refTypeID'],
                                   item.attrib['refID'],
                                   item.attrib['argID1'],
                                   item.attrib['balance']))

        root.clear()
        self.db.commit()





api = eve_api()
api.import_api_key('api_key')
api.connect_db('transactions.db')
api.import_journal()
api.import_transactions()
