import { MainStatistic } from "app/modules/main-statistic/types";

export const SET_MAIN_STATISTIC = "SET_MAIN_STATISTIC";

export function setMainStatistic(statistic: MainStatistic) {
	return { type: SET_MAIN_STATISTIC, statistic };
}

const initialState: MainStatistic = {
	total: 0,
	filtered: 0,
};

function mainStatistic(state: MainStatistic = initialState, action: any) {
	switch (action.type) {
		case SET_MAIN_STATISTIC:
			return {
				...action.statistic,
			};

		default:
			return state;
	}
}

export default mainStatistic;
