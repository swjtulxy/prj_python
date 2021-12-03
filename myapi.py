from fastapi import FastAPI

from mem_access import get_men
app = FastAPI()


@app.get('/mem/addresslist={addresslist}')
def calcalate(addresslist: str=None):
    res = {"res" : get_men(addresslist.split('_'))}
    return res

if __name__=='__main__':
    import uvicorn
    uvicorn.run(app=app,
    host="0.0.0.0",
    port=9999,
    workers=1)
