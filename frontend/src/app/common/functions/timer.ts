export class Timer {
	timerId: NodeJS.Timeout;
	start: number;
	remaining: number;
	paused = false;
	cb: (...args: any[]) => void;

	constructor(cb: (...args: any[]) => void, delay: number) {
		this.cb = cb;
		this.remaining = delay;

		this.start = Date.now();
		this.timerId = setTimeout(this.cb, this.remaining);
	}

	pause = () => {
		clearTimeout(this.timerId);
		this.paused = true;
		this.remaining -= Date.now() - this.start;
	};

	resume = () => {
		this.start = Date.now();
		clearTimeout(this.timerId);
		this.paused = false;
		this.timerId = setTimeout(this.cb, this.remaining);
	};

	close = () => {
		clearTimeout(this.timerId);
	};
}
