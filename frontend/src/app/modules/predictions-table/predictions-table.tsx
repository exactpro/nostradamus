import Icon, { IconType } from "app/common/components/icon/icon";
import { ObjectWithUnknownFields } from "app/common/types/http.types";
import React from "react";
import "./predictions-table.scss";
import DropdownElement from "app/common/components/native-components/dropdown-element/dropdown-element";
import TableCell from "app/modules/predictions-table/table-cell/table-cell";

interface IProps {
	tableData: ObjectWithUnknownFields[];
	totalCount: number;
	onChangePage: (pageIndex: number, limit: number) => void;
}

interface IState {
	limit: number;
	currentPage: number;
}

class PredictionsTable extends React.Component<IProps, IState> {
	state = {
		limit: 20,
		currentPage: 1,
	};

	onChangeLimit = (limit: string) => {
		const newLimit = Number(limit);
		const oldLimit = this.state.limit;
		let newCurrentPage = Math.ceil((this.state.currentPage * oldLimit) / newLimit);

		if (oldLimit > newLimit) {
			newCurrentPage = ((this.state.currentPage - 1) * oldLimit) / newLimit + 1;
		}

		if ((newCurrentPage - 1) * newLimit > this.props.totalCount) {
			newCurrentPage = Math.ceil(this.props.totalCount / newLimit);
		}

		this.setState({
			limit: newLimit,
			currentPage: newCurrentPage,
		});
		this.props.onChangePage(newCurrentPage, newLimit);
	};

	setPage = (newPage: number) => () => {
		const currentPage = newPage < 1 ? 1 : newPage;
		this.setState({ currentPage });
		this.props.onChangePage(currentPage, this.state.limit);
	};

	render() {
		const { tableData } = this.props;

		const columnsNames: string[] = Object.keys(tableData[0]);

		return (
			<div className="predictions-table">
				{this.renderTableHeader()}

				{/* data table */}
				<div className="predictions-table__scrollable-container">
					<table className="predictions-table__table predictions-table__table">
						<thead>
							<tr>
								{columnsNames.map((columnName, index) => (
									<th key={index}>{columnName}</th>
								))}
							</tr>
						</thead>

						<tbody>
							{tableData.map((item, index) => (
								<tr key={index}>
									{columnsNames.map((columnName) => {
										const message = String(item[columnName]);
										return <TableCell key={message} message={message} />;
									})}
								</tr>
							))}
						</tbody>
					</table>
				</div>
			</div>
		);
	}

	renderTableHeader = () => {
		const { currentPage, limit } = this.state;

		const rowFrom = (currentPage - 1) * limit + 1;
		let rowTo = currentPage * limit;

		const totalPage = Math.ceil(this.props.totalCount / limit);

		if (rowTo > this.props.totalCount) {
			rowTo = this.props.totalCount;
		}

		return (
			<div className="predictions-table__pagination predictions-table-pagination">
				<div className="predictions-table-pagination__field">
					<span className="predictions-table-pagination__label">Show by</span>
					<DropdownElement
						dropDownValues={["20", "50", "100"]}
						onChange={this.onChangeLimit}
						writable={false}
						value={this.state.limit.toString()}
					/>
				</div>

				<div className="predictions-table-pagination__field">
					<span className="predictions-table-pagination__label">Shown</span>

					{totalPage > 1 && (
						<button
							onClick={this.setPage(currentPage - 1)}
							disabled={currentPage === 1}
							className="predictions-table-pagination__button"
						>
							<Icon type={IconType.left} size={16} className="predictions-table-pagination__icon" />
						</button>
					)}

					<div>
						<span className="predictions-table-pagination__value">
							{rowFrom}-{rowTo}
						</span>
						<span className="predictions-table-pagination__label">of</span>
						<span className="predictions-table-pagination__value">{this.props.totalCount}</span>
					</div>

					{totalPage > 1 && (
						<button
							onClick={this.setPage(currentPage + 1)}
							disabled={currentPage === totalPage}
							className="predictions-table-pagination__button"
						>
							<Icon
								type={IconType.right}
								size={16}
								className="predictions-table-pagination__icon"
							/>
						</button>
					)}
				</div>
			</div>
		);
	};
}

export default PredictionsTable;
