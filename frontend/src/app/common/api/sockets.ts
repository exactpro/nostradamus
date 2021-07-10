import { getDataFromLocalStorage } from "app/common/functions/local-storage";
import { User } from "app/common/types/user.types";

export enum SocketEventType {
	updateCountIssues = 'UPDATE_COUNT_ISSUES'
}

export interface SocketEvent {
	type: SocketEventType;
	data?: unknown;
}

type callback = (...params: unknown[]) => unknown;

export default class SocketClient {

	private token = "";

	private readonly host: string;
	private ws: WebSocket | undefined = undefined;
	private subscribers: Map<SocketEventType, callback> = new Map()

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

	private startWatching() {
		const sockets = this.ws || this.connectToSocket();

		sockets.addEventListener("message", (event: MessageEvent) => {
			let eventData: SocketEvent;

			try {
				eventData = JSON.parse(event.data);
			} catch (e) {
				eventData = { type: event.data };
			}

			const cb = this.subscribers.get(eventData.type);

			if (cb) {
				cb((event.data as SocketEvent).data)
			}
		})
	}

	subscribeToEvent(type: SocketEventType, cb: callback) {
		if (this.subscribers.size === 0) {
			this.startWatching();
		}

		// TODO: add ability set some subscribes to one event type
		if (this.subscribers.has(type)) {
			throw new Error('This type event already has subscriber');
		}

		this.subscribers.set(type, cb);
	}

	unsubscribe(type: SocketEventType) {
		this.subscribers.delete(type);

		if (this.subscribers.size === 0) {
			this.ws?.close();
			this.ws = undefined;
		}
	}
}
