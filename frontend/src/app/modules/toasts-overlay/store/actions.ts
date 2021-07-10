import {
	Toast,
	ToastConfig,
	ToastStyle, ToastWithActionsParams
} from "app/modules/toasts-overlay/store/types";

const DEFAULT_CONFIG: ToastConfig = {
	time: 5000,
	hideable: true, // grammar error, but coll description
};

export const addToast = (message: string, style: ToastStyle, config?: ToastConfig) =>
	({
		type: "TOASTS_ADD_TOAST",
		toast: {
			message,
			style,
			actionToast: false,
			buttons: {},
			config: {
				...DEFAULT_CONFIG,
				...config,
			},
		} as Toast,
	} as const);


export const addToastWithAction = (
	newToast: ToastWithActionsParams
) =>
	({
		type: "TOASTS_ADD_TOAST",
		toast: {
			message: newToast.message,
			style: newToast.style,
			actionToast: true,
			buttons: newToast.buttons,
			config: {
				...DEFAULT_CONFIG,
				time: 300000,
			},
			outerId: newToast.outerId,
		} as Toast,
	} as const);

export const removeToast = (toastId: number) =>
	({
		type: "TOASTS_REMOVE_TOAST",
		toastId,
	} as const);

export const removeToastByOuterId = (toastId: number) =>
	({
		type: "TOASTS_REMOVE_TOAST_BY_OUTER_ID",
		toastId,
	} as const);
