export enum HttpStatus {
	PREVIEW = 'preview',
	LOADING = 'loading',
	FINISHED = 'finished',
	RELOADING = 'reloading',
	FAILED = 'failed'
}

export interface HttpException {
	detail: string
	code: number
	message: string
}

export class HttpError extends Error implements HttpException {

	code: number;
	detail: string;

	constructor(exception: HttpException) {
		super(exception.message);

		this.code = exception.code;
		this.message = exception.message;
		this.detail = exception.detail || '';
	}

}

interface FieldError {
	name: string;
	errors: string[]
}

export class HttpValidationError extends HttpError {

	fields: FieldError[];
	detailArr: string[] = [];

	constructor(props: HttpException, fields: FieldError[]) {
		super(props);

		this.fields = fields;
		this.detail = this.fields[0].errors[0];
		this.fields.forEach(({errors})=>this.detailArr.push(...errors))
	}

}
