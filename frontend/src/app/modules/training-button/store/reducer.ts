import { InferValueTypes } from 'app/common/store/utils';
import { HttpStatus } from 'app/common/types/http.types';
import { TrainingModelState } from 'app/modules/training-button/store/types';
import * as actions from './actions';

const initialState: TrainingModelState = {
	status: HttpStatus.PREVIEW,
};

type trainingModelStoreActionsType = ReturnType<InferValueTypes<typeof actions>>;

function trainingModel(state: TrainingModelState = initialState, action: trainingModelStoreActionsType) {
	switch (action.type) {
		case 'TRAINING_MODEL_SET_STATUS':
			return {
				...state,
				status: action.status,
			};

		default:
			return state;
	}
}

export default trainingModel;
