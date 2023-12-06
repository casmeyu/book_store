from fastapi import FastAPI, Request, HTTPException, status


async def private(request: Request, next):
    print("this is a private route:", request)
    print("request", request)
    print("request state", request.state)
    request.state["IS_PUBLIC"] = True
    if request.state["IS_PUBLIC"] == True or request.state["user"]:
        print("IS PUBLIC")
        return next()
    
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="unauthorized access")


async def public(request: Request, next):
    print("this is a public route")
    request.state["IS_PUBLIC"] = True
    return next()