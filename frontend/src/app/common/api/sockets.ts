import { getDataFromLocalStorage } from 'app/common/functions/local-storage';
import { User } from 'app/common/types/user.types';

export class SocketClient {

	private token: string = '';

	host: string;
	ws: WebSocket | undefined = undefined;

	constructor() {
		if (process.env.NODE_ENV === 'development') {
			this.host = 'ws://127.0.0.1';
		} else {
			this.host = window.location.protocol === 'http:' ? 'ws://' : 'wss://'
			this.host += window.location.host;
		}
	}

	connectToSocket(): WebSocket  {
		let user = getDataFromLocalStorage<User>('user');

		if (user) {
			this.token = user.token;
		}

		this.ws = new WebSocket(`${this.host}/ws/extractor_listener/?token=${this.token}`);
		return this.ws;
	}

	startMonitor(type: string, cb: (data: any) => void) {
		let sockets = this.ws || this.connectToSocket();

		sockets.addEventListener(type, (event: any) => {
			cb(event.data);
		});
	}
}
