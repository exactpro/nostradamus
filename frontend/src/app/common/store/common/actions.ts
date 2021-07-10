import { CommonStore } from "app/common/store/common/types";

export const updateCommonStatuses = (statuses: Partial<CommonStore>) => ({
	type: 'UPDATE_COMMON_STATUSES',
	statuses
} as const)

export const resetCommonStatuses = () => ({
	type: 'RESET_COMMON_STATUSES',
} as const)
