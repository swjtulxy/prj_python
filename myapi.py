from fastapi import FastAPI
import part1
import part2
app = FastAPI()

physicalMemory = {}
tlb = []
pageTable = []
pageFaultCounter = 0
tlbHitCounter = 0
addressReadCounter = 0

def get_men(addr):
    global physicalMemory
    global tlb
    global pageTable
    global pageFaultCounter
    global tlbHitCounter
    global addressReadCounter
    outputFile = open('output.txt', 'w')
    print(addr)
    tlbHit = 0
    pageTableTrue = 0
    logicalAddress = int(addr)
    print(logicalAddress)
    offset = logicalAddress & 255
    pageOriginal = logicalAddress & 65280
    pageNumber = pageOriginal >> 8
    print("Logical address is: " + str(logicalAddress) + "\nPageNumber is: " + str(pageNumber) + "\nOffset: " + str(offset))
    addressReadCounter += 1

    tlbHit, Pa, data = part1.checkTLB(pageNumber, physicalMemory, offset, logicalAddress, tlb, addressReadCounter, outputFile)

    if tlbHit == 1:
        tlbHitCounter += 1

    if tlbHit != 1:
        pageTableTrue, Pa, data = part1.checkPageTable(pageNumber, logicalAddress, offset, addressReadCounter, pageTable, physicalMemory, outputFile)

    if pageTableTrue != 1 and tlbHit != 1:
        print("This is a page fault!")
        part2.pageFaultHandler(pageNumber, tlb, pageTable, physicalMemory)
        pageFaultCounter += 1
        _, Pa, data = part1.checkTLB(pageNumber, physicalMemory, offset, logicalAddress, tlb, addressReadCounter, outputFile)


    pageFaultRate = pageFaultCounter / addressReadCounter
    tlbHitRate = tlbHitCounter / addressReadCounter
    outStr = 'Number of translated address: ' + str(addressReadCounter) + '\n' + 'Number of page fault: ' + str(
        pageFaultCounter) + '\n' + 'Page fault rate: ' + str(pageFaultRate) + '\n' + 'Number of TLB hits: ' + str(
        tlbHitCounter) + '\n' + 'TLB hit rate: ' + str(tlbHitRate) + '\n'
    print(outStr)
    outputFile.write(outStr)
    # print(physicalMemory)
    # print(tlb)
    # print (pageTable)
    outputFile.close()
    res = {
        "VA" : logicalAddress,
        "PageNumber" : pageNumber,
        "offset" : offset,
        "Pa" : Pa,
        "Data" : data,
        "tlbHit" : tlbHit,
        "pageTableTrue" : pageTableTrue,
        "pageFaultRate" : pageFaultRate,
        "tlbHitRate" : tlbHitRate,
    }
    
    return res

@app.get('/mem/addr={addr}')
def calcalate(addr: str=None):
    return get_men(addr)

@app.get('/tlb')
def gettlb():
    res = {"res" : tlb}
    return res

@app.get('/pageTable')
def getPagetable():
    res = {"res" : pageTable}
    return res

if __name__=='__main__':
    import uvicorn
    uvicorn.run(app=app,
    host="0.0.0.0",
    port=9999,
    workers=1)
