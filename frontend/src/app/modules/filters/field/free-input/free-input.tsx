import ExactMatch from 'app/modules/filters/field/exact-match/exact-match';
import { FilterFieldBase } from 'app/modules/filters/field/field-type';

import 'app/modules/filters/field/free-input/free-input.scss';
import { FilterField } from 'app/modules/filters/field/filter-field.class';
import ResetValue from 'app/modules/filters/field/reset-value/reset-value';
import { UpdateFieldFunction } from 'app/modules/filters/filters.class';
import cn from 'classnames';
import React from 'react';

interface Props {
	className?: string
	field: FilterFieldBase,
	updateFunction: UpdateFieldFunction
}

interface State {
	value: string
}

class FreeInput extends React.Component<Props, State> {

	field: FilterField;

	constructor(props: Props) {
		super(props);

		this.field = new FilterField(this.props.field, this.props.updateFunction);
	}

	resetValue = () => {
		this.field.resetValue();
		this.forceUpdate();
	};

	handleChanges = (event: React.ChangeEvent<HTMLInputElement>) => {
		this.field.updateValue(event.target.value);
		this.forceUpdate()
	};

	toggleExactMatch = () => {
		this.field.toggleExactMatch();
		this.forceUpdate();
	};

	render() {
		let field = this.field;

		return (
			<div className="field">
				<ExactMatch exactMatch={field.exact_match} onToggle={this.toggleExactMatch} />

				<input
					type="text"
					className={cn('free-input', this.props.className)}
					name={field.name}
					value={String(field.current_value)}
					onChange={this.handleChanges}
					onBlur={this.field.applyField}
				/>

				<ResetValue onClick={this.resetValue} className="field__reset" />
			</div>
		);
	}
}

export default FreeInput;
