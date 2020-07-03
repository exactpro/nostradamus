import React from 'react';

import './header.scss';

interface HeaderProps {
  pageTitle: string
}

class Header extends React.Component<HeaderProps> {

  render() {
    return (
      <header className="header">
        <h1 className="header__title">
          {this.props.pageTitle}
        </h1>

        {
          this.props.children
        }
      </header>
    );
  }
}

export default Header;
