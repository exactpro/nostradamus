import React, { useState } from "react";
import InputElement from "app/modules/settings/elements/input-element/input-element";
import Icon, { IconSize, IconType } from "app/common/components/icon/icon";
import { FilterElementType } from "app/modules/settings/elements/elements-types";
import InputEntityElement from "app/modules/settings/elements/input-entity-element/input-entity-element";
import { RootStore } from "app/common/types/store.types";
import { useSelector } from "react-redux";
import { MarkUpEntitiesElement } from "app/modules/settings/parts/training/store/types";
import "./table-form.scss";

interface Props {
	isAllowedEditing: boolean;
	onAddTableRow: (element: MarkUpEntitiesElement) => void;
}

export default function TableForm(props: Props) {
	// Selector for extraction entities names list from store
	const entityNames = useSelector(
		(store: RootStore) => store.settings.settingsTrainingStore.markup_entities.entity_names
	);
	// Form's state
	const [areaOfTesting, setAreaOfTesting] = useState<string>("");
	const [entities, setEntities] = useState<string[]>([]);

	// Methods for modification form state
	const deleteEntity = (index: number) => {
		entities.splice(index, 1);
		setEntities([...entities]);
	};
	const addEntity = (entity: string) => {
		setEntities([...entities, entity]);
	};

	const addTableRow = () => {
		props.onAddTableRow({
			entities,
			area_of_testing: areaOfTesting,
		});
		setEntities([]);
		setAreaOfTesting("");
	};

	return (
		<div className="settings-training-table-form">
			<div className="settings-training-table-form__wrapper">
				<div className="settings-training-table-form-input">
					<p className="settings-training-table-form__field-title">Name</p>
					<InputElement
						type={props.isAllowedEditing ? FilterElementType.simple : FilterElementType.disabled}
						value={areaOfTesting}
						placeholder="Name"
						onChange={(value) => setAreaOfTesting(value)}
						onClear={() => setAreaOfTesting("")}
						style={{ width: "90%" }}
					/>
				</div>

				<div className="settings-training-table-form-select">
					<p className="settings-training-table-form__field-title">Entities</p>
					<div className="settings-training-table-form-select__select-wrapper">
						<InputEntityElement
							type={props.isAllowedEditing ? FilterElementType.simple : FilterElementType.disabled}
							onChange={addEntity}
							onClear={deleteEntity}
							onClearAll={() => setEntities([])}
							dropDownValues={entityNames}
							values={entities}
						/>
						<button
							type="button"
							className="settings-training-table-form__add-position"
							onClick={addTableRow}
							disabled={!(areaOfTesting && entities.length)}
						>
							<Icon size={IconSize.small} type={IconType.close} />
						</button>
					</div>
				</div>
			</div>
		</div>
	);
}
