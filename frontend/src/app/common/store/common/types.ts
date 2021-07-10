export interface CommonStore {
	isLoadedIssuesStatus: boolean;
	isIssuesExist: boolean;
	isSearchingModelFinished: boolean;
	isModelFounded: boolean;
}

export interface InitialApiResponse {
	issues_exists: boolean;
}
