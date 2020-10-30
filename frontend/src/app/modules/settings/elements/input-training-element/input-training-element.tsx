/* eslint-disable jsx-a11y/no-noninteractive-tabindex */
import React, { Component } from "react";
import cn from "classnames";
import {
	FilterElementType,
	FilterDropdownType,
} from "app/modules/settings/elements/elements-types";
import SelectWindow from "app/common/components/native-components/select-window/select-window";
import Icon, { IconSize, IconType } from "app/common/components/icon/icon";
import "app/modules/settings/elements/input-training-element/input-training-element.scss";

interface InputTrainingElementProps {
	type: FilterElementType;
	onChange: (value: string) => void;
	onClear: (index: number) => void;
	onClearAll: () => void;
	values: string[];
	dropDownValues: string[];
}

interface InputTrainingElementState {
	isSelectWindowOpen: boolean;
	isSelectedListOpen: boolean;
}

export default class InputTrainingElement extends Component<
	InputTrainingElementProps,
	InputTrainingElementState
> {
	// eslint-disable-next-line react/static-property-placement
	static defaultProps = {
		type: FilterElementType.simple,
		dropDownValues: Object.values(FilterDropdownType),
	};

	// eslint-disable-next-line no-undef
	timerID: NodeJS.Timeout | null = null;
	inputTrainingElementRef: React.RefObject<HTMLDivElement> = React.createRef();
	allowedEditing = false;

	constructor(props: InputTrainingElementProps) {
		super(props);

		this.state = {
			isSelectWindowOpen: false,
			isSelectedListOpen: false,
		};
	}

	onFocusTrainingElement = (): void => {
		if (!this.allowedEditing) return;
		if (this.timerID) clearTimeout(this.timerID);
		this.setState({ isSelectWindowOpen: true });
	};

	onBlurTrainingElement = (): void => {
		this.timerID = setTimeout(
			() => this.setState({ isSelectWindowOpen: false, isSelectedListOpen: false }),
			0
		);
	};

	openSelectedValuesList = (): void => {
		this.setState((state) => ({
			isSelectedListOpen: !state.isSelectedListOpen,
		}));
	};

	selectDropdownValue = (value: string, isChecked: boolean) => (): void => {
		const { values, onChange } = this.props;
		if (isChecked) {
			this.deleteValueBlock(values.findIndex((item) => item === value))();
			return;
		}
		onChange(value);
	};

	deleteValueBlock = (index: number) => (): void => {
		const { values, onClear } = this.props;
		const { isSelectedListOpen } = this.state;

		if (this.inputTrainingElementRef.current && values.length === 1 && isSelectedListOpen) {
			this.inputTrainingElementRef.current.blur();
		}
		onClear(index);
	};

	deleteAllValueBlocks = (): void => {
		const { onClearAll } = this.props;
		onClearAll();
	};

	renderValueBlocks = (content: string, index: number): React.ReactNode => {
		return (
			<div key={index} className="input-training-element-value-block">
				<div className="input-training-element-value-block__wrapper">
					<p className="input-training-element-value-block__number">{index + 1}</p>
					<p className="input-training-element-value-block__content">{content}</p>
					{this.allowedEditing && (
						<button
							type="button"
							className="input-training-element-value-block__close"
							onClick={this.deleteValueBlock(index)}
						>
							<Icon size={IconSize.small} type={IconType.close} />
						</button>
					)}
				</div>
			</div>
		);
	};

	isStrIncludesSubstr = (str: string, substr: string): boolean =>
		str.toLowerCase().includes(substr.toLowerCase());

	render() {
		const { values, dropDownValues, type } = this.props;
		const { isSelectedListOpen, isSelectWindowOpen } = this.state;

		this.allowedEditing = [FilterElementType.simple, FilterElementType.edited].includes(type);

		const dropdownValues = isSelectedListOpen ? values : dropDownValues;

		return (
			<div
				className="input-training-element"
				tabIndex={0}
				onFocus={this.onFocusTrainingElement}
				onBlur={this.onBlurTrainingElement}
				ref={this.inputTrainingElementRef}
			>
				{this.allowedEditing && (
					<div className="input-training-element-icons">
						<button
							type="button"
							className="input-training-element-icons__close"
							onClick={this.deleteAllValueBlocks}
						>
							<Icon size={IconSize.small} type={IconType.close} />
						</button>
						<Icon
							className={cn("input-training-element-icons__down", {
								"input-training-element-icons__down_rotated": isSelectWindowOpen,
							})}
							size={IconSize.small}
							type={IconType.down}
						/>
					</div>
				)}

				<div
					className={cn(
						"input-training-element-block-container",
						`input-training-element-block-container_${type}`
					)}
				>
					{values.length ? (
						[...values].splice(0, 2).map((item, index) => this.renderValueBlocks(item, index))
					) : (
						<p className="input-training-element-block-container__placeholder">Entities Name</p>
					)}
				</div>

				{values.length > 2 && this.allowedEditing && (
					<button
						type="button"
						className="input-training-element__spread-button"
						onClick={this.openSelectedValuesList}
					>
						+{values.length - 2}
						more
					</button>
				)}

				{isSelectWindowOpen && (
					<div className="input-training-element__select-window">
						<SelectWindow
							selectWindowAllValues={dropdownValues}
							selectWindowCheckedValues={values}
							searchable={!isSelectedListOpen}
							onSelectValue={this.selectDropdownValue}
						/>
					</div>
				)}
			</div>
		);
	}
}
