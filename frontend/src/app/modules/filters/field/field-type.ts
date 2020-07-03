export enum FiltrationType {
	Date = 'date',
	Numeric = 'numeric',
	Dropdown = 'drop-down',
	String = 'string'
}

export type FilterFieldStringValue = string;
export type FilterFieldDropdownValue = string[];
export type FilterFieldNumberValue = [number | null, number | null];
export type FilterFieldDateValue = [Date | null, Date | null];

export type ValueUnion = FilterFieldStringValue | FilterFieldDropdownValue | FilterFieldNumberValue | FilterFieldDateValue;

export interface FilterFieldBase {
	name: string,
	filtration_type: FiltrationType,
	exact_match: boolean,
	current_value: ValueUnion,
	values?: FilterFieldDropdownValue
}
