import { getDataFromLocalStorage } from "app/common/functions/local-storage";
import { User } from "app/common/types/user.types";

export default class SocketClient {
	private token = "";

	host: string;
	ws: WebSocket | undefined = undefined;

	constructor() {
		if (process.env.NODE_ENV === "development") {
			this.host = "ws://127.0.0.1";
		} else {
			this.host = window.location.protocol === "http:" ? "ws://" : "wss://";
			this.host += window.location.host;
		}
	}

	connectToSocket(): WebSocket {
		const user = getDataFromLocalStorage<User>("user");

		if (user) {
			this.token = user.token;
		}

		this.ws = new WebSocket(`${this.host}/ws/extractor_listener/?token=${this.token}`);
		return this.ws;
	}

	// TODO: eslint-disable-next-line
	// eslint-disable-next-line
	startMonitor(type: string, cb: (data: any) => void): void {
		const sockets = this.ws || this.connectToSocket();

		// TODO: eslint-disable-next-line
		// eslint-disable-next-line
		sockets.addEventListener(type, (event: any) => {
			// TODO: @typescript-eslint/no-unsafe-member-access
			// eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
			cb(event.data);
		});
	}
}
