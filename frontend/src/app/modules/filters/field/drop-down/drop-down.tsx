import Tooltip from "app/common/components/tooltip/tooltip";
import { Timer } from "app/common/functions/timer";
import ExactMatch from "app/modules/filters/field/exact-match/exact-match";

import "app/modules/filters/field/drop-down/drop-down.scss";
import { FilterFieldBase, FilterFieldDropdownValue } from "app/modules/filters/field/field-type";
import { FilterField } from "app/modules/filters/field/filter-field.class";
import ResetValue from "app/modules/filters/field/reset-value/reset-value";
import { UpdateFieldFunction } from "app/modules/filters/filters.class";
import cn from "classnames";
import React, { RefObject } from "react";
import SelectWindow from "app/common/components/native-components/select-window/select-window";

interface Props {
	className?: string;
	field: FilterFieldBase;
	updateFunction: UpdateFieldFunction;
}

interface State {
	isOpen: boolean;
	isCheckedVariantList: boolean;
	search: string;
}

class DropDown extends React.PureComponent<Props, State> {
	state = {
		isOpen: false,
		isCheckedVariantList: false,
		search: "",
	};

	field: FilterField;

	timer: Timer | null = null;
	fieldRef: RefObject<HTMLDivElement> = React.createRef();

	constructor(props: Props) {
		super(props);
		this.field = new FilterField(this.props.field, this.props.updateFunction);
	}

	toggleItem = (newItem: string, checked: boolean) => () => {
		const current_value = [...(this.field.current_value as FilterFieldDropdownValue)];

		if (checked) {
			const index = current_value.findIndex((item) => item === newItem);
			current_value.splice(index, 1);
		} else {
			current_value.push(newItem);
		}

		this.field.updateValue([...current_value]);

		if (this.state.isCheckedVariantList && current_value.length === 0) {
			this.fieldRef.current && this.fieldRef.current.blur();
		} else {
			this.forceUpdate();
		}
	};

	resetItem = (item: string) => () => {
		this.toggleItem(item, true)();
		this.field.applyField();

		this.setState({ isOpen: false });
	};

	resetValue = () => {
		this.field.toggleExactMatch(false);
		this.field.updateValue([]);
		this.field.applyField();

		this.setState({ isOpen: false });
	};

	toggleExactMatch = () => {
		this.field.toggleExactMatch();
		this.forceUpdate();
	};

	openCheckedVariant = () => {
		this.setState({ isCheckedVariantList: true });
	};

	changeSearchRequest = (event: React.ChangeEvent<HTMLInputElement>) => {
		this.setState({ search: event.target.value });
	};

	onFocus = () => {
		this.stopHidden();

		this.setState({ isOpen: true });
	};

	stopHidden = () => {
		this.timer && this.timer.close();
	};

	onBlur = () => {
		// for don't removing dropdown, when set focus at the quick search
		this.timer = new Timer(() => {
			this.setState({
				isCheckedVariantList: false,
				isOpen: false,
			});

			this.field.applyField();
		}, 1);
	};

	render() {
		const value = this.field.current_value as FilterFieldDropdownValue;
		let values = this.state.isCheckedVariantList
			? value
			: (this.field.values as FilterFieldDropdownValue);

		if (!this.state.isCheckedVariantList && this.state.search) {
			values = values.filter(
				(item) => item.toLowerCase().indexOf(this.state.search.toLowerCase()) > -1
			);
		}

		return (
			<div
				className={cn("drop-down", "field", this.props.className, {
					"drop-down_without-left-padding": value.length >= 2,
				})}
				tabIndex={0}
				onBlur={this.onBlur}
				ref={this.fieldRef}
				onFocus={this.onFocus}
			>
				{value.length > 1 && (
					<ExactMatch exactMatch={this.field.exact_match} onToggle={this.toggleExactMatch} />
				)}

				{[...value].splice(0, 2).map((item, index) =>
					item ? (
						<Tooltip duration={1} message={item} key={index}>
							<span className="drop-down__value-item">
								<span className="drop-down__value-item-text">{item}</span>

								<ResetValue
									className="drop-down__value-item-remove"
									onClick={this.resetItem(item)}
								/>
							</span>
						</Tooltip>
					) : null
				)}

				{value.length > 2 && (
					<span className="drop-down__more-value" onClick={this.openCheckedVariant}>
						+ {value.length - 2} more
					</span>
				)}

				{value.length === 0 && (
					<span className="drop-down__no-value">Select {this.field.name}</span>
				)}

				<ResetValue onClick={this.resetValue} className="drop-down__reset" />

				{this.state.isOpen && (
					<div className="drop-down__select-window">
						<SelectWindow
							selectWindowAllValues={values}
							selectWindowCheckedValues={value}
							onSelectValue={this.toggleItem}
							searchable={!this.state.isCheckedVariantList}
						/>
					</div>
				)}
			</div>
		);
	}
}

export default DropDown;
