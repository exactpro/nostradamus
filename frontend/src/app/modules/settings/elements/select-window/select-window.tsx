import React, {useState, ReactNode} from "react";
import "app/modules/settings/elements/select-window/select-window.scss";
import Icon, { IconType, IconSize } from "app/common/components/icon/icon";
import { isStrIncludesSubstr, caseInsensitiveStringCompare } from "app/common/functions/helper";

interface SelectWindowProps{
    selectWindowAllValues: string[],
    selectWindowCheckedValues: string[],
    searchable: boolean,
    onSelectValue: (value: string, isChecked: boolean)=>()=>void,
    placeholder?: string,
    children?: ReactNode,
}

// Should consider to use this component on all select windows
export default function SelectWindow(props: SelectWindowProps){
    let [quickSearchValue, changeQuickSearchValue] = useState(""); 
    return (
        <div className="select-window-element">

        {
            props.searchable && 
            <div className="select-window-element__search">
                <input  type="text"
                        value={quickSearchValue}
                        onChange={(e) => changeQuickSearchValue(e.target.value)} 
                        className="select-window-element__search-input" 
                        placeholder={props.placeholder || "Quick search"}/>
                <Icon type={IconType.find} size={IconSize.small} className="select-window-element__search-icon" />
            </div>
        }
        <div className="select-window-element__wrapper">
        {
        props.selectWindowAllValues
             .filter(str => isStrIncludesSubstr(str.toString(), quickSearchValue))
             .sort((a, b) => caseInsensitiveStringCompare(a,b))
             .map((item,index)=>{
            let checked = props.selectWindowCheckedValues.findIndex(checkedItem => checkedItem === item) > -1; 
            return (
            <label key={index} className="select-window-element__item">
                <input
                className="select-window-element__browser-checkbox"
                type="checkbox" 
                checked={checked}
                onChange={props.onSelectValue(item, checked)}
                />

                <span className="select-window-element__checkbox">
                {
                    checked &&
                    <Icon type={IconType.check} className="select-window-element__check-mark" size={IconSize.small} />
                }
                </span>

                {item}
            </label>
        )})
        }
        </div>
        {
            props.children
        }
    </div>
    )
} 