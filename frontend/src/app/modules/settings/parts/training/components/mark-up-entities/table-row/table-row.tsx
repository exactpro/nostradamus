import React, { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import Icon, { IconType, IconSize } from "app/common/components/icon/icon";
import { FilterElementType } from "app/modules/settings/elements/elements-types";
import InputElement from "app/modules/settings/elements/input-element/input-element";
import InputEntityElement from "app/modules/settings/elements/input-entity-element/input-entity-element";
import { RootStore } from "app/common/types/store.types";
import { MarkUpEntitiesElement } from "app/modules/settings/parts/training/store/types";
import "./table-row.scss";

interface Props {
	status: FilterElementType;
	areaOfTesting: string;
	markUpEntities: string[];
	isAllowedRowEditing: boolean;
	isDisabled: boolean;

	onEditTableRowData: () => void;
	onDeleteTableRow: () => void;
	onAcceptTableRowDataEditing: (entity: MarkUpEntitiesElement) => void;
}

export default function TableRow(props: Props) {
	// Table row state data
	const entitiesNames = useSelector(
		(store: RootStore) => store.settings.settingsTrainingStore.markup_entities.entity_names
	);
	const [tableRowStatus, setTableRowStatus] = useState<FilterElementType>(props.status);
	const [areaOfTesting, setAreaOfTesting] = useState<string>(props.areaOfTesting);
	const [markUpEntities, setMarkUpEntities] = useState<string[]>(props.markUpEntities);

	// Table row methods
	const changeHoverStatus = (isHovered = true) => () => {
		if (!props.isDisabled || props.status === FilterElementType.edited) {
			return;
		}
		isHovered ? setTableRowStatus(FilterElementType.hovered) : setTableRowStatus(props.status);
	};

	const addEntity = (entity: string) => {
		setMarkUpEntities([...markUpEntities, entity]);
	};

	const removeEntity = (index: number) => {
		markUpEntities.splice(index, 1);
		setMarkUpEntities([...markUpEntities]);
	};

	const removeAllEntities = () => {
		setMarkUpEntities([]);
	};

	const acceptTableRowEditing = () => {
		props.onAcceptTableRowDataEditing({ area_of_testing: areaOfTesting, entities: markUpEntities });
	};

	// Effect hook for renew state data with props change
	useEffect(() => {
		setTableRowStatus(props.status);
		setAreaOfTesting(props.areaOfTesting);
		setMarkUpEntities(props.markUpEntities);
	}, [props.status, props.areaOfTesting, props.markUpEntities]);

	return (
		<div
			className="settings-training-table-row"
			onMouseLeave={changeHoverStatus(false)}
			onMouseMove={changeHoverStatus()}
		>
			<div className="settings-training-table-row__input">
				<InputElement
					type={tableRowStatus === FilterElementType.hovered ? tableRowStatus : props.status}
					value={tableRowStatus === FilterElementType.edited ? areaOfTesting : props.areaOfTesting}
					onChange={setAreaOfTesting}
					onClear={() => setAreaOfTesting("")}
				/>
			</div>
			<div className="settings-training-table-row__select">
				<InputEntityElement
					type={tableRowStatus === FilterElementType.hovered ? tableRowStatus : props.status}
					onChange={addEntity}
					onClear={removeEntity}
					onClearAll={removeAllEntities}
					dropDownValues={entitiesNames}
					values={
						tableRowStatus === FilterElementType.edited ? markUpEntities : props.markUpEntities
					}
				/>
				{tableRowStatus === FilterElementType.edited && (
					<button
						type="button"
						className="settings-training-table-row__accept-button"
						onClick={acceptTableRowEditing}
						disabled={!(areaOfTesting && markUpEntities.length)}
					>
						<Icon type={IconType.check} size={IconSize.normal} />
					</button>
				)}
			</div>

			{tableRowStatus === FilterElementType.hovered && (
				<div className="settings-training-table-row__edit-wrapper">
					<button
						type="button"
						className="settings-training-table-row__edit-button"
						onClick={props.onEditTableRowData}
						disabled={props.isAllowedRowEditing}
					>
						<Icon type={IconType.edit2} size={IconSize.normal} />
					</button>

					<button
						type="button"
						className="settings-training-table-row__delete-button"
						onClick={props.onDeleteTableRow}
						disabled={props.isAllowedRowEditing}
					>
						<Icon type={IconType.delete} size={IconSize.normal} />
					</button>
				</div>
			)}
		</div>
	);
}
