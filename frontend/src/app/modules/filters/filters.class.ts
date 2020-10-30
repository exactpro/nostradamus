import { FilterFieldBase, FiltrationType } from "app/modules/filters/field/field-type";
import { getFieldEmptyValue, setFieldValue } from "app/modules/filters/field/field.helper-function";

export class FiltersClass {
	fields: FilterFieldBase[];

	constructor(fields: FilterFieldBase[]) {
		this.fields = this.setFilter(fields);
	}

	resetAllFields = () => {
		this.fields = this.fields.map((field: FilterFieldBase) => ({
			...field,
			current_value: setFieldValue(
				field.filtration_type,
				getFieldEmptyValue(field.filtration_type)
			),
		}));
	};

	updateField(updatedField: FilterFieldBase) {
		this.fields = this.fields.map((field) => {
			if (field.name === updatedField.name) {
				return { ...updatedField };
			}

			return field;
		});
	}

	setFilter(filter: FilterFieldBase[]): FilterFieldBase[] {
		return filter.map((field) => {
			if (field.filtration_type === FiltrationType.String && field.current_value instanceof Array) {
				field.current_value = field.current_value.length
					? (field.current_value as [string])[0]
					: "";
			}
			if (field.filtration_type === FiltrationType.Dropdown) field.values!.sort();
			return field;
		});
	}
}

export type UpdateFieldFunction = (field: FilterFieldBase) => void;

export type ApplyFilterFieldValue = string | string[];
export type ApplyFilterFieldRangeValue = [number | Date | null, number | Date | null];
