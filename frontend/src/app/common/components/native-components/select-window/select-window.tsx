/* eslint-disable react/require-default-props */
import React, { useState, ReactNode, ReactElement } from "react";
import "app/common/components/native-components/select-window/select-window.scss";
import Icon, { IconType, IconSize } from "app/common/components/icon/icon";
import { isStrIncludesSubstr, caseInsensitiveStringCompare } from "app/common/functions/helper";

interface SelectWindowProps {
	selectWindowAllValues: string[];
	selectWindowCheckedValues: string[];
	searchable: boolean;
	onSelectValue: (value: string, isChecked: boolean) => () => void;
	placeholder?: string;
	children?: ReactNode;
}

// Should consider to use this component on all select windows

export default function SelectWindow(props: SelectWindowProps): ReactElement {
	const [quickSearchValue, changeQuickSearchValue] = useState<string>("");

	const { searchable, placeholder, children, selectWindowAllValues } = props;

	const filteredValues: string[] = [...selectWindowAllValues].filter((str) =>
		isStrIncludesSubstr(str.toString(), quickSearchValue)
	);

	return (
		<div className="select-window-element">
			{searchable && (
				<div className="select-window-element__search">
					<input
						type="text"
						value={quickSearchValue}
						onChange={(e) => changeQuickSearchValue(e.target.value)}
						className="select-window-element__search-input"
						placeholder={placeholder || "Quick search"}
					/>
					<Icon
						type={IconType.find}
						size={IconSize.small}
						className="select-window-element__search-icon"
					/>
				</div>
			)}
			<div className="select-window-element__wrapper">
				{filteredValues.length > 500 ? (
					<p className="select-window-element__too-much">Too much variants, use search</p>
				) : (
					filteredValues
						.sort((a, b) => caseInsensitiveStringCompare(a, b))
						.map((item) => {
							const checked =
								props.selectWindowCheckedValues.findIndex((checkedItem) => checkedItem === item) >
								-1;
							return (
								<label
									htmlFor={`select-window-element_${item}`}
									key={item}
									className="select-window-element__item"
								>
									<input
										id={`select-window-element_${item}`}
										className="select-window-element__browser-checkbox"
										type="checkbox"
										checked={checked}
										onChange={props.onSelectValue(item, checked)}
									/>

									<span className="select-window-element__checkbox">
										{checked && (
											<Icon
												type={IconType.check}
												className="select-window-element__check-mark"
												size={IconSize.small}
											/>
										)}
									</span>

									{item}
								</label>
							);
						})
				)}
			</div>
			{children}
		</div>
	);
}
