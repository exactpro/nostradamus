import { HttpStatus } from 'app/common/types/http.types';

export type Terms = { [key: string]: number };

export interface SignificantTermsStateInitial {
	metrics: string[],
	chosen_metric: string | null,
	terms: Terms
}

export interface SignificantTermsState {
	status: HttpStatus,
	metrics: string[],
	chosen_metric: string | null,
	terms: Terms
}
