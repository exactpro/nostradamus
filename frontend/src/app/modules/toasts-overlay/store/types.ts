export enum ToastStyle {
	Info = "_info",
	Success = "_success",
	Error = "_error",
	Warning = "_warn",
}

export interface ToastConfig {
	time: number;
	hideable: boolean;
}

export interface ToastButton {
	buttonName: string;
	callBack: () => void;
}

export interface Toast {
	id: number;
	outerId?: number;
	message: string;
	style: ToastStyle;
	config: ToastConfig;
	actionToast: boolean;
	buttons: ToastButton[];
}

export interface ToastStore {
	newToastId: number;
	toastList: Toast[];
}
