import { HttpStatus } from 'app/common/types/http.types';

export const trainingModelSetStatus = (status: HttpStatus) => ({
	type: 'TRAINING_MODEL_SET_STATUS',
	status
} as const);
