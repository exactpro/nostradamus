import {
	FilterFieldBase,
	FilterFieldDropdownValue,
	FiltrationType,
	ValueUnion,
} from "app/modules/filters/field/field-type";
import {
	checkFieldIsFilled,
	getFieldEmptyValue,
	setFieldValue,
} from "app/modules/filters/field/field.helper-function";
import { UpdateFieldFunction } from "app/modules/filters/filters.class";

export class FilterField {
	// base properties
	name: string;
	type: FiltrationType;
	exact_match: boolean;
	current_value: ValueUnion;
	values?: FilterFieldDropdownValue;

	// extended properties (don't send to server)
	updateFunction: UpdateFieldFunction;

	constructor(field: FilterFieldBase, updateFunction: UpdateFieldFunction) {
		this.name = field.name;
		this.type = field.type;
		this.exact_match = field.exact_match;

		if (field.current_value && checkFieldIsFilled(field.type, field.current_value)) {
			this.current_value = setFieldValue(field.type, field.current_value);
		} else {
			this.current_value = setFieldValue(
				field.type,
				getFieldEmptyValue(this.type)
			);
		}

		if (field.values) {
			this.values = field.values.map(val => String(val));
		}

		this.updateFunction = updateFunction;
	}

	toggleExactMatch = (exactMatch?: boolean) => {
		this.exact_match = exactMatch === undefined ? !this.exact_match : exactMatch;
		this.applyField();
	};

	updateValue = (newValue: ValueUnion) => {
		this.current_value = setFieldValue(this.type, newValue);
	};

	resetValue = () => {
		this.toggleExactMatch(false);
		this.updateValue(getFieldEmptyValue(this.type));
		this.applyField();
	};

	applyField = () => {
		const field: FilterFieldBase = {
			name: this.name,
			type: this.type,
			exact_match: this.exact_match,
			current_value: setFieldValue(this.type, this.current_value),
		};
		if (this.values) field.values = this.values;
		this.updateFunction(field);
	};
}
