import React, { useState } from "react";
import cn from "classnames";
import { MarkUpEntitiesElement } from "app/modules/settings/parts/training/store/types";
import { FilterElementType } from "app/modules/settings/elements/elements-types";
import TableRow from "app/modules/settings/parts/training/components/mark-up-entities/table-row/table-row";
import TableForm from "app/modules/settings/parts/training/components/mark-up-entities/table-form/table-form";
import "./mark-up-entities.scss";

interface Props {
	markUpEntities: MarkUpEntitiesElement[];
	isAllowedEditing: boolean;

	onModifyMarkUpEntities: (entity: MarkUpEntitiesElement[]) => void;
}

export default function MarkUpEntities(props: Props) {
	// Component state
	const invalidIndex = -1;
	const [editIndex, setEditIndex] = useState<number>(invalidIndex);

	// Method determines row's background-color
	const getTableRowParityStatus = (index: number) => {
		if (index === editIndex) {
			return FilterElementType.edited;
		}
		if (index % 2 === 1) {
			return FilterElementType.odd;
		}
		return FilterElementType.even;
	};

	// Handlers for markup_entities modification
	const acceptTableRowDataEditing = (index: number) => (entity: MarkUpEntitiesElement) => {
		const newMarkUpEntities = [...props.markUpEntities];
		newMarkUpEntities[index] = { ...entity };
		props.onModifyMarkUpEntities([...newMarkUpEntities]);
		setEditIndex(invalidIndex);
	};

	const deleteTableRow = (index: number) => () => {
		const newMarkUpEntities = [...props.markUpEntities];
		newMarkUpEntities.splice(index, 1);
		props.onModifyMarkUpEntities([...newMarkUpEntities]);
	};

	const addTableRow = (entity: MarkUpEntitiesElement) => {
		props.onModifyMarkUpEntities([...props.markUpEntities, entity]);
	};

	return (
		<div
			className={cn("settings-training-table", {
				"settings-training-table_disabled": !props.isAllowedEditing,
			})}
		>
			<TableForm isAllowedEditing={props.isAllowedEditing} onAddTableRow={addTableRow} />
			<div className="settings-training-table-main">
				{props.markUpEntities.map((entity: MarkUpEntitiesElement, index: number) => (
					<TableRow
						key={index}
						status={getTableRowParityStatus(index)}
						areaOfTesting={entity.area_of_testing}
						markUpEntities={entity.entities}
						isAllowedRowEditing={props.isAllowedEditing && editIndex !== invalidIndex}
						isDisabled={props.isAllowedEditing}
						onAcceptTableRowDataEditing={acceptTableRowDataEditing(index)}
						onEditTableRowData={() => setEditIndex(index)}
						onDeleteTableRow={deleteTableRow(index)}
					/>
				))}
			</div>
		</div>
	);
}
