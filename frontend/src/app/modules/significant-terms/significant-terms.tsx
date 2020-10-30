import { TagCloud } from "app/common/components/charts/tag-cloud/tag-cloud";
import CircleSpinner from "app/common/components/circle-spinner/circle-spinner";
import { HttpStatus } from "app/common/types/http.types";
import { Terms } from "app/modules/significant-terms/store/types";
import DropdownElement from "app/common/components/native-components/dropdown-element/dropdown-element";
import React from "react";

import "./significant-terms.scss";

interface Props {
	status: HttpStatus;
	onChangeMetric: (period: string) => void;
	metrics: string[];
	chosen_metric: string | null;
	terms: Terms;
}

export default function SignificantTerms(props: Props) {
	const changeSelect = (str: string) => {
		props.onChangeMetric(str);
	};

	return (
		<div className="significant-terms">
			<div className="significant-terms__select-wrapper">
				{props.chosen_metric && (
					<DropdownElement
						writable={false}
						dropDownValues={props.metrics}
						value={props.chosen_metric}
						onChange={changeSelect}
					/>
				)}
			</div>

			{props.status === HttpStatus.FINISHED && <TagCloud tags={props.terms} />}

			{props.status === HttpStatus.RELOADING && <CircleSpinner alignCenter />}
		</div>
	);
}
