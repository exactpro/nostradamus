import {
	FilterFieldDateValue,
	FilterFieldDropdownValue,
	FilterFieldNumberValue,
	FiltrationType,
	ValueUnion,
} from 'app/modules/filters/field/field-type';

export const getFieldEmptyValue = (filtration_type: FiltrationType): ValueUnion => {
	switch (filtration_type) {
		case FiltrationType.String:
			return '';

		case FiltrationType.Numeric:
		case FiltrationType.Date:
			return [null, null];

		case FiltrationType.Dropdown:
			return [];
	}
};

export const setFieldValue = (filtration_type: FiltrationType, newValue: ValueUnion): ValueUnion => {
	switch (filtration_type) {
		case FiltrationType.String:
			return newValue;

		case FiltrationType.Numeric:
			return [ (newValue as FilterFieldNumberValue)[0], (newValue as FilterFieldNumberValue)[1] ];

		case FiltrationType.Date:
			let newValueLink = newValue as FilterFieldDateValue;
			let start = (newValueLink)[0] ? new Date(newValueLink[0]) : null;
			let end = (newValueLink)[1] ? new Date(newValueLink[1]) : null;
			if(end instanceof Date) { end.setHours(23,59,59); }
			return [ start, end ];

		case FiltrationType.Dropdown:
			return [...newValue as FilterFieldDropdownValue];
	}
};

export const checkFieldIsFilled = (filtration_type: FiltrationType, value: ValueUnion): boolean => {
	switch (filtration_type) {
		case FiltrationType.String:
			return !!value;

		case FiltrationType.Numeric:
		case FiltrationType.Date:
			let valueTyped = value as FilterFieldNumberValue | FilterFieldDateValue;
			return !!(valueTyped[0] || valueTyped[1]);

		case FiltrationType.Dropdown:
			return !!(value as FilterFieldDropdownValue).length;
	}
};
