export default class QueueGenerator<T> {
    private dispatchFunction: (arg: T)=>void;
    private beforeEachFunction: (()=>void) | undefined; 
    private queueTime: number;
    private argumentsQueueArr: T[] = [];
    private queueTimerPointer: NodeJS.Timer | null = null;

    constructor(dispatchFunction: (arg: T)=>void, time: number, beforeEachFunction?: ()=>void) {
        this.dispatchFunction = dispatchFunction;
        this.beforeEachFunction = beforeEachFunction;
        this.queueTime = time;
    }

    public pushQueueArguments(arg: T | T[]) {
        Array.isArray(arg) ? this.argumentsQueueArr.push(...arg) : this.argumentsQueueArr.push(arg);
        if (!this.queueTimerPointer) this.startQueueAction();
    }

    private startQueueAction() {
        this.queueTimerPointer = setInterval(() => {
            this.dispatchFunction(this.argumentsQueueArr[0]);
            this.argumentsQueueArr.shift();

            if (!this.argumentsQueueArr.length) this.clearQueueInterval()
            else if (this.beforeEachFunction) this.beforeEachFunction();
        }, this.queueTime);
    }

    private clearQueueInterval() {
        if (this.queueTimerPointer) clearInterval(this.queueTimerPointer);
        this.queueTimerPointer = null;
    }

}