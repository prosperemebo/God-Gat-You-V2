'use client';

import { Fragment, Suspense } from 'react';
import { AppProgressBar as ProgressBar } from 'next-nprogress-bar';

function LoadingBar() {
  return (
    <Fragment>
      <Suspense>
        <ProgressBar
          height='5px'
          color='#dcff14'
          options={{ showSpinner: false }}
          shallowRouting
        />
      </Suspense>
    </Fragment>
  );
}

export default LoadingBar;
