import { analysisAndTrainingReducers } from "app/common/store/analysis-and-training/reducers";
import descriptionAssessmentReducer from "app/common/store/description-assessment/reducer";

import { authReducer } from "app/common/store/auth/reducers";
import { commonReducer } from "app/common/store/common/reducers";
import { qaMetricsPageReducer } from "app/common/store/qa-metrics/reducers";
import { generalSettingsStore } from "app/common/store/settings/reducers";
import { trainingReducers } from "app/common/store/traininig/reducers";
import virtualAssistantReducer from "app/common/store/virtual-assistant/reducers";
import { RootStore } from "app/common/types/store.types";
import { toastsReducers } from "app/modules/toasts-overlay/store/reducer";
import { connectRouter, routerMiddleware } from "connected-react-router";
import { createBrowserHistory, History } from "history";
import { applyMiddleware, combineReducers, createStore } from "redux";
import { composeWithDevTools } from "redux-devtools-extension";
import thunk from "redux-thunk";

export const history = createBrowserHistory();

const rootReducers = (history: History) =>
	combineReducers({
		toasts: toastsReducers,
		auth: authReducer,
		settings: generalSettingsStore,
		virtualAssistant: virtualAssistantReducer,
		qaMetricsPage: qaMetricsPageReducer,
		common: commonReducer,
		analysisAndTraining: analysisAndTrainingReducers,
		descriptionAssessment: descriptionAssessmentReducer,
		training: trainingReducers,
		router: connectRouter(history),
	});

function configureStore(preloadedState?: RootStore) {
	const store = createStore(
		rootReducers(history),
		preloadedState,
		composeWithDevTools(
			applyMiddleware(
				routerMiddleware(history), // for dispatching history actions
				thunk
			)
		)
	);
	return store;
}

const store = configureStore();

export default store;
