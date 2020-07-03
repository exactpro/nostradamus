import { qaMetricsPageReducer } from 'app/common/store/qa-metrics/reducers';
import { toastsReducers } from 'app/modules/toasts-overlay/store/reducer';
import {applyMiddleware, combineReducers, createStore} from 'redux';
import thunk from 'redux-thunk';
import {composeWithDevTools} from "redux-devtools-extension";
import {connectRouter, routerMiddleware} from 'connected-react-router';

import {analysisAndTrainingStore} from 'app/common/store/analysis-and-training/reducers';
import {authReducer} from "app/common/store/auth/reducers";
import {settingsReducer} from "app/common/store/settings/reducers";
import {virtualAssistantReducer} from "app/common/store/virtual-assistant/reducers";
import {createBrowserHistory, History} from "history";
import {RootStore} from "app/common/types/store.types";

export const history = createBrowserHistory();

const rootReducers = (history: History) => combineReducers({
  analysisAndTraining: analysisAndTrainingStore,
  toasts: toastsReducers,
  auth: authReducer,
  settings: settingsReducer,
  virtualAssistant: virtualAssistantReducer,
  qaMetricsPage: qaMetricsPageReducer,
  router: connectRouter(history),
});

function configureStore(preloadedState?: RootStore) {
  let store = createStore(
    rootReducers(history),
    preloadedState,
    composeWithDevTools(applyMiddleware(
      routerMiddleware(history), // for dispatching history actions
      thunk
    ))
  );
  return store
}

const store = configureStore();

export default store;
