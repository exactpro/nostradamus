export enum HttpStatus {
	PREVIEW = "preview",
	LOADING = "loading",
	FINISHED = "finished",
	RELOADING = "reloading",
	WARNING = "warning",
	FAILED = "failed",
}

export interface ObjectWithUnknownFields<T = unknown> {
	[key: string]: T
}

export interface HttpException {
	detail: string;
	code: number;
	message: string;
}

export class HttpError extends Error implements HttpException {
	code: number;
	detail: string;

	constructor(exception: HttpException) {
		super(exception.message);

		this.code = exception.code;
		this.message = exception.message;
		this.detail = exception.detail || "";
	}
}

export interface HTTPFieldValidationError {
	name: string;
	errors: string[];
}

export class HTTPValidationError {

	fields: HTTPFieldValidationError[]

	constructor(fields: HTTPFieldValidationError[]) {
		this.fields = fields;
	}
}
