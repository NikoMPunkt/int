import uasyncio as asyncio 


class App1:
    def __init__(self):
        self.event = asyncio.Event()
        self.__task_list = []
    
    async def coro1(self):
        while True:
            print('App1 > coro1')
            await asyncio.sleep(3)
            
    async def coro2(self):
        while True:
            await asyncio.sleep(2)
            print('App1 > coro2')
            
    async def wrapper(self):
        self.__task_list.append(asyncio.create_task(self.coro1()))
        self.__task_list.append(asyncio.create_task(self.coro2()))
        await self.__task_list[-1]
    
    async def Cancel_all_tasks(self):
        for task in self.__task_list:
            task.cancel()
            try:
                await task
                print(id(task), 'not an awaiting task!')
            except asyncio.CancelledError:
                print(id(task), 'gracefully terminated')
        
    async def Run(self):
        asyncio.create_task(self.wrapper())
       
    
class App2:
    def __init__(self):
        self.event = asyncio.Event()
        self.__task_list = []
    
    async def coro1(self):
        while True:
            print('App2 > coro1')
            await asyncio.sleep(2)
            self.event.set()
            self.event.clear()
            
    async def coro2(self):
        while True:
            await self.event.wait()
            print('App2 > coro2 (event)')
            
    async def coro3(self):
        while True:
            await asyncio.sleep(10)
            print('App2 > coro3')
            
    async def wrapper(self):
        self.__task_list.append(asyncio.create_task(self.coro1()))
        self.__task_list.append(asyncio.create_task(self.coro2()))
        self.__task_list.append(asyncio.create_task(self.coro3()))
        await self.__task_list[-1]
    
    async def Cancel_all_tasks(self):
        for task in self.__task_list:
            task.cancel()
            try:
                await task
                print(id(task), 'not an awaiting task!')
            except asyncio.CancelledError:
                print(id(task), 'gracefully terminated')
        
    
    async def Run(self):
        asyncio.create_task(self.wrapper())
        
       
class Stopper:
    def __init__(self):
        self.event = asyncio.Event()
    
    async def stop(self):
        await asyncio.sleep(3)
        print('STOPPER SET!')
        
class Main:
    def __init__(self):
        self.event = asyncio.Event()
        self.app1 = App1()
        self.app2 = App2()
        self.stopper = Stopper()
        
    async def wrapper(self):
        asyncio.create_task(self.app1.Run())
        asyncio.create_task(self.app2.Run())
        await self.stopper.stop()
    
    async def Run(self):
        await self.wrapper()
        
        await self.app1.Cancel_all_tasks()
        await self.app2.Cancel_all_tasks()
        print('End MAIN')
        await asyncio.sleep(30)
       

main = Main()
asyncio.run(main.Run())
