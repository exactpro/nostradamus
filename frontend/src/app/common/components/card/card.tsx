import 'app/common/components/card/card.scss';
import CircleSpinner from 'app/common/components/circle-spinner/circle-spinner';
import { isOneOf } from 'app/common/functions/helper';
import cn from 'classnames';
import React from 'react';
import { HttpStatus } from 'app/common/types/http.types';

// TODO: refactor to meet solid principles (left only view, remove unnecessary logic)
interface CardProps {
	title?: string;
	className?: string;
	previewImage?: string;
	hoverHeader?: boolean; // for the situation, when we have elements in header of card
	status: HttpStatus;
	isErrorAvailable?: boolean // display content, even if request is failed
}

class Card extends React.Component<CardProps> {

	static defaultProps = {
		status: HttpStatus.FINISHED,
	};

	render() {

		const { status } = this.props;
		const S = HttpStatus;

		let whenShowPreviewManage = [S.PREVIEW, S.LOADING];
		if (!this.props.isErrorAvailable) {
			whenShowPreviewManage.push(S.FAILED);
		}
		let cardContentStyle = {
			backgroundImage: isOneOf(status, whenShowPreviewManage) ? `url(${this.props.previewImage})` : 'none',
		};

		return (
			<section className={cn('card', this.props.className)}>
				{
					this.props.title &&
          <h3 className="card__title" style={{ position: this.props.hoverHeader ? 'absolute' : 'static' }}>
						{this.props.title}
          </h3>
				}

				{
					isOneOf(status, [S.LOADING]) &&
          <CircleSpinner alignCenter />
				}

				<div className="card__content" style={cardContentStyle}>
					{(status === S.FINISHED || (this.props.isErrorAvailable && (status === S.FAILED))) && this.props.children}
				</div>
			</section>
		);
	}
}

export default Card;
