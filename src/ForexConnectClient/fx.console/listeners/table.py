import forexconnect as fx
from listeners import Counter, EventHook

class TableListener(fx.TableListener):
    def __init__(self):
        super(TableListener, self).__init__()
        self.refcount = Counter(1)
        self.instrument = ""
        self.offers = []
        self.onOffersChanged = EventHook()

    def __del__(self):
        pass

    def addRef(self):
        self.refcount.increment()
        ref = self.refcount.value
        return ref

    def release(self):
        self.refcount.decrement()
        ref = self.refcount.value
        if self.refcount.value == 0:
            del self
        return ref

    def setInstrument(self, instrument):
        self.instrument = instrument

    def onAdded(self, rowID, rowData):
        print "onAdded"

    def onChanged(self, rowID, rowData):        
        rowData.__class__ = fx.IO2GOfferRow
        self.onOffersChanged.fire(rowData)

    def onDelete(self, rowID, rowData):
        print "onDelete"

    def onStatusChanged(self, status):
        print status

    def printOffers(self, offersTable, instrument):
        iterator = fx.IO2GTableIterator()
        offerRow = offersTable.getNextRow(iterator)
        while offerRow:
            self.printOffer(offerRow, instrument)
            offerRow.release()
            offerRow = offersTable.getNextRow(iterator)

    def printOffer(self, offerRow, instrument):
        if self.instrument == offerRow.getInstrument():
            print offerRow.getInstrument(), "Bid: ", offerRow.getBid(), "Ask: ", offerRow.getAsk()

    def subscribeEvents(self, manager):
        offersTable = manager.getTable(fx.O2GTable.Offers)
        offersTable.__class__ = fx.IO2GOffersTable
        offersTable.subscribeUpdate(fx.O2GTableUpdateType.Update, self)

    def unsubscribeEvents(self, manager):
        offersTable = manager.getTable(fx.O2GTable.Offers)
        offersTable.__class__ = fx.IO2GOffersTable
        offersTable.unsubscribeUpdate(fx.O2GTableUpdateType.Update, self)
